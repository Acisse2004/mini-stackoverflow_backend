from django.db import models
from django.conf import settings


class Tag(models.Model):
    """Tag pour classer les questions — US013"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    """
    Question posée par un utilisateur connecté.
    US004, US005, US006, US007
    """
    title = models.CharField(max_length=300)
    description = models.TextField()          # Contenu Markdown
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    vote_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def answer_count(self):
        return self.answers.count()

    @property
    def is_resolved(self):
        return self.answers.filter(is_best=True).exists()
