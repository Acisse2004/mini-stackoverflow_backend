from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    US001, US002, US003, US014
    """
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        default=None
    )
    bio = models.TextField(blank=True, default='')

    def __str__(self):
        return self.username

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def answer_count(self):
        return self.answers.count()
