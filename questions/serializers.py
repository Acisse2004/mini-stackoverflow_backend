from rest_framework import serializers
from .models import Question, Tag
from users.serializers import UserMinimalSerializer

class TagSerializer(serializers.ModelSerializer):
    question_count = serializers.ReadOnlyField()
    class Meta:
        model = Tag
        fields = ('id', 'name', 'description', 'question_count')

class QuestionListSerializer(serializers.ModelSerializer):
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
    author = UserMinimalSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    # On accepte maintenant des NOMS de tags (texte), pas des ID.
    # S'ils n'existent pas encore en base, ils sont crees automatiquement.
    tag_ids = serializers.ListField(
        child=serializers.CharField(), write_only=True, source='tag_names', required=False
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

    def _get_or_create_tags(self, tag_names):
        tags = []
        for name in tag_names:
            name = name.strip().lower()
            if not name:
                continue
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        return tags

    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        question = Question.objects.create(**validated_data)
        question.tags.set(self._get_or_create_tags(tag_names))
        return question

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_names is not None:
            instance.tags.set(self._get_or_create_tags(tag_names))
        return instance