from django.contrib import admin
from .models import Answer, Comment, Vote


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'question', 'is_best', 'vote_count', 'created_at')
    list_filter = ('is_best',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'answer', 'created_at')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'answer', 'question', 'created_at')
