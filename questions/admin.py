from django.contrib import admin
from .models import Question, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'question_count')
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'vote_count', 'answer_count', 'is_resolved', 'created_at')
    list_filter = ('tags',)
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)
