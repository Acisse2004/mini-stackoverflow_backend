from django.urls import path
from .views import (
    AnswerListCreateView,
    AnswerDetailView,
    AnswerVoteView,
    MarkBestAnswerView,
    CommentListCreateView,
    CommentDetailView,
)

urlpatterns = [
    # Réponses d'une question
    path('questions/<int:question_id>/answers/',
         AnswerListCreateView.as_view(), name='answer-list'),

    # Détail / vote / meilleure réponse
    path('answers/<int:pk>/',       AnswerDetailView.as_view(),   name='answer-detail'),
    path('answers/<int:pk>/vote/',  AnswerVoteView.as_view(),     name='answer-vote'),
    path('answers/<int:pk>/best/',  MarkBestAnswerView.as_view(), name='answer-best'),

    # Commentaires
    path('answers/<int:answer_id>/comments/',
         CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/',
         CommentDetailView.as_view(),     name='comment-detail'),
]
