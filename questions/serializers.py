from rest_framework import serializers
from .models import Question, Tag
from users.serializers import UserMinimalSerializer


class TagSerializer(serializers.ModelSerializer):
    question_count = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'description', 'question_count')


class QuestionListSerializer(serializers.ModelSerializer):
    """Serializer léger pour la liste des questions — US005"""
    author = UserMinimalSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    answer_count = serializers.ReadOnlyField()
    is_resolved = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = (
            'id', 'title', 'author', 'tags',
            'vote_count', 'answer_count', 'is_resolved', 'created_at'
        )


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour le détail d'une question — US007"""
    author = UserMinimalSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, source='tags'
    )
    answer_count = serializers.ReadOnlyField()
    is_resolved = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = (
            'id', 'title', 'description', 'author', 'tags', 'tag_ids',
            'vote_count', 'answer_count', 'is_resolved',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'vote_count', 'created_at', 'updated_at')

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        question = Question.objects.create(**validated_data)
        question.tags.set(tags)
        return question

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
