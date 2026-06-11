from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Question, Tag
from .serializers import QuestionListSerializer, QuestionDetailSerializer, TagSerializer
from .filters import QuestionFilter


class QuestionListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/questions/         — Liste + filtre + recherche (US005, US006, US012)
    POST /api/questions/         — Créer une question (US004)
    """
    queryset = Question.objects.select_related('author').prefetch_related('tags', 'answers')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = QuestionFilter
    search_fields = ('title', 'description')          # US012 — recherche mot-clé
    ordering_fields = ('created_at', 'vote_count')    # US006 — tri
    ordering = ('-created_at',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionDetailSerializer
        return QuestionListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/questions/<id>/  — Détail d'une question (US007)
    PUT    /api/questions/<id>/  — Modifier (auteur seulement)
    DELETE /api/questions/<id>/  — Supprimer (auteur seulement)
    """
    queryset = Question.objects.select_related('author').prefetch_related('tags')
    serializer_class = QuestionDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': 'Non autorisé.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': 'Non autorisé.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class QuestionVoteView(APIView):
    """
    POST /api/questions/<id>/vote/
    US009 — Voter pour une question (+1 ou -1)
    Body : { "value": 1 }  ou  { "value": -1 }
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({'error': 'Question introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        value = request.data.get('value')
        if value not in (1, -1):
            return Response({'error': 'La valeur doit être 1 ou -1.'}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si l'utilisateur a déjà voté (via l'app answers)
        from answers.models import Vote
        existing = Vote.objects.filter(user=request.user, question=question).first()

        if existing:
            if existing.value == value:
                # Annuler le vote
                question.vote_count -= value
                question.save()
                existing.delete()
                return Response({'message': 'Vote annulé.', 'vote_count': question.vote_count})
            else:
                # Changer de vote
                question.vote_count += (value - existing.value)
                question.save()
                existing.value = value
                existing.save()
        else:
            Vote.objects.create(user=request.user, question=question, value=value)
            question.vote_count += value
            question.save()

        return Response({'vote_count': question.vote_count})


# ── Tags ─────────────────────────────────────────────────────────────────────

class TagListView(generics.ListAPIView):
    """
    GET /api/questions/tags/
    US013 — Liste des tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('name',)


class TagQuestionListView(generics.ListAPIView):
    """
    GET /api/questions/tags/<name>/questions/
    US013 — Questions filtrées par tag
    """
    serializer_class = QuestionListSerializer

    def get_queryset(self):
        tag_name = self.kwargs['name']
        return Question.objects.filter(
            tags__name__iexact=tag_name
        ).select_related('author').prefetch_related('tags', 'answers')
