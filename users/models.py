from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        default=None
    )
    bio = models.TextField(blank=True, default='')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def answer_count(self):
        return self.answers.count()