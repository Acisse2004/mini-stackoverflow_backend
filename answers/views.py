from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Answer, Comment, Vote
from .serializers import AnswerSerializer, CommentSerializer, VoteSerializer
from questions.models import Question


class AnswerListCreateView(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Answer.objects.filter(
            question_id=self.kwargs['question_id']
        ).select_related('author').prefetch_related('comments__author')

    def perform_create(self, serializer):
        question = generics.get_object_or_404(Question, pk=self.kwargs['question_id'])
        serializer.save(author=self.request.user, question=question)


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.select_related('author').prefetch_related('comments')
    serializer_class = AnswerSerializer
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


class AnswerVoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        answer = generics.get_object_or_404(Answer, pk=pk)
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        value = serializer.validated_data['value']

        existing = Vote.objects.filter(user=request.user, answer=answer).first()

        if existing:
            if existing.value == value:
                answer.vote_count -= value
                answer.save()
                existing.delete()
                return Response({'message': 'Vote annule.', 'vote_count': answer.vote_count})
            else:
                answer.vote_count += (value - existing.value)
                answer.save()
                existing.value = value
                existing.save()
        else:
            Vote.objects.create(user=request.user, answer=answer, value=value)
            answer.vote_count += value
            answer.save()

        return Response({'vote_count': answer.vote_count})


class MarkBestAnswerView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        answer = generics.get_object_or_404(Answer, pk=pk)
        question = answer.question

        if question.author != request.user:
            return Response(
                {'error': 'Seul l auteur de la question peut choisir la meilleure reponse.'},
                status=status.HTTP_403_FORBIDDEN
            )

        Answer.objects.filter(question=question, is_best=True).update(is_best=False)

        if answer.is_best:
            answer.is_best = False
        else:
            answer.is_best = True
        answer.save()

        return Response({'is_best': answer.is_best})


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Comment.objects.filter(
            answer_id=self.kwargs['answer_id']
        ).select_related('author')

    def perform_create(self, serializer):
        answer = generics.get_object_or_404(Answer, pk=self.kwargs['answer_id'])
        serializer.save(author=self.request.user, answer=answer)


class CommentDetailView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'error': 'Non autorise.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)