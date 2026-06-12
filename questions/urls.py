from django.urls import path
from .views import (
    QuestionListCreateView,
    QuestionDetailView,
    QuestionVoteView,
    TagListView,
    TagQuestionListView,
)

urlpatterns = [
    # Questions
    path('',                          QuestionListCreateView.as_view(), name='question-list'),
    path('<int:pk>/',                 QuestionDetailView.as_view(),     name='question-detail'),
    path('<int:pk>/vote/',            QuestionVoteView.as_view(),       name='question-vote'),

    # Tags
    path('tags/',                     TagListView.as_view(),            name='tag-list'),
    path('tags/<str:name>/questions/', TagQuestionListView.as_view(),   name='tag-questions'),
]
