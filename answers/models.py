from django.db import models
from django.conf import settings


class Answer(models.Model):
    """
    Réponse à une question.
    US008, US009, US011
    """
    question = models.ForeignKey(
        'questions.Question',
        on_delete=models.CASCADE,
        related_name='answers'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    content = models.TextField()          # Contenu Markdown
    is_best = models.BooleanField(default=False)
    vote_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_best', '-vote_count', 'created_at']

    def __str__(self):
        return f"Réponse de {self.author} à '{self.question.title}'"


class Comment(models.Model):
    """
    Commentaire sur une réponse.
    US010
    """
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire de {self.author}"


class Vote(models.Model):
    """
    Vote (+1 / -1) sur une réponse ou une question.
    US009
    """
    VOTE_CHOICES = ((1, 'Upvote'), (-1, 'Downvote'))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='votes',
        null=True, blank=True
    )
    question = models.ForeignKey(
        'questions.Question',
        on_delete=models.CASCADE,
        related_name='votes',
        null=True, blank=True
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Un utilisateur ne peut voter qu'une fois par réponse/question
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'answer'],
                condition=models.Q(answer__isnull=False),
                name='unique_vote_per_answer'
            ),
            models.UniqueConstraint(
                fields=['user', 'question'],
                condition=models.Q(question__isnull=False),
                name='unique_vote_per_question'
            ),
        ]

    def __str__(self):
        target = f"réponse {self.answer_id}" if self.answer else f"question {self.question_id}"
        return f"Vote {self.value} de {self.user} sur {target}"
