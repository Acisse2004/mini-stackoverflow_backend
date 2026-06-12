from rest_framework import serializers
from .models import Answer, Comment, Vote
from users.serializers import UserMinimalSerializer


class CommentSerializer(serializers.ModelSerializer):
    """US010 — Commentaire sur une réponse"""
    author = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')


class AnswerSerializer(serializers.ModelSerializer):
    """US008, US009, US011 — Réponse avec ses commentaires"""
    author = UserMinimalSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = (
            'id', 'author', 'content', 'is_best',
            'vote_count', 'comments', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'author', 'is_best', 'vote_count', 'created_at', 'updated_at')


class VoteSerializer(serializers.Serializer):
    """US009 — Envoyer un vote"""
    value = serializers.ChoiceField(choices=[1, -1])
