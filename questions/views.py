from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import Question, Tag
from .serializers import QuestionListSerializer, QuestionDetailSerializer, TagSerializer
from .filters import QuestionFilter

class QuestionListCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    filterset_class = QuestionFilter
    search_fields = ('title', 'description')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionDetailSerializer
        return QuestionListSerializer

    def get_queryset(self):
        queryset = Question.objects.select_related('author').prefetch_related('tags', 'answers')
        sort = self.request.query_params.get('sort', 'recent')
        if sort == 'recent':
            queryset = queryset.order_by('-created_at')
        elif sort == 'votes':
            queryset = queryset.order_by('-vote_count')
        elif sort == 'unanswered':
            queryset = queryset.filter(answers__isnull=True).order_by('-created_at')
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.select_related('author').prefetch_related('tags')
    serializer_class = QuestionDetailSerializer
    permission_classes = (AllowAny,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': 'Non autorise.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': 'Non autorise.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class QuestionVoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({'error': 'Question introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        value = request.data.get('value')
        if value not in (1, -1):
            return Response({'error': 'La valeur doit etre 1 ou -1.'}, status=status.HTTP_400_BAD_REQUEST)
        from answers.models import Vote
        existing = Vote.objects.filter(user=request.user, question=question).first()
        if existing:
            if existing.value == value:
                question.vote_count -= value
                question.save()
                existing.delete()
                return Response({'message': 'Vote annule.', 'vote_count': question.vote_count})
            else:
                question.vote_count += (value - existing.value)
                question.save()
                existing.value = value
                existing.save()
        else:
            Vote.objects.create(user=request.user, question=question, value=value)
            question.vote_count += value
            question.save()
        return Response({'vote_count': question.vote_count})

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('name',)
    permission_classes = (AllowAny,)

class TagQuestionListView(generics.ListAPIView):
    serializer_class = QuestionListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        tag_name = self.kwargs['name']
        return Question.objects.filter(
            tags__name__iexact=tag_name
        ).select_related('author').prefetch_related('tags', 'answers')