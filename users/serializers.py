from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """US001 — Inscription"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Les mots de passe ne correspondent pas.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """US002 — Connexion"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Identifiants incorrects.')

        if not user.check_password(data['password']):
            raise serializers.ValidationError('Identifiants incorrects.')

        if not user.is_active:
            raise serializers.ValidationError('Compte désactivé.')

        data['user'] = user
        return data


class UserQuestionSerializer(serializers.Serializer):
    """Version allegee d'une question, pour l'afficher dans le profil."""
    id = serializers.IntegerField()
    title = serializers.CharField()
    vote_count = serializers.IntegerField()


class UserAnswerSerializer(serializers.Serializer):
    """Version allegee d'une reponse, pour l'afficher dans le profil."""
    question = serializers.IntegerField(source='question_id')
    question_title = serializers.CharField(source='question.title')
    is_best = serializers.BooleanField()


class UserProfileSerializer(serializers.ModelSerializer):
    """US003, US014 — Profil + statistiques"""
    question_count = serializers.ReadOnlyField()
    answer_count = serializers.ReadOnlyField()
    vote_count = serializers.ReadOnlyField()
    questions = UserQuestionSerializer(many=True, read_only=True)
    answers = UserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'bio', 'avatar',
            'question_count', 'answer_count', 'vote_count',
            'questions', 'answers', 'date_joined'
        )
        read_only_fields = ('id', 'date_joined')


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializer léger utilisé dans les autres apps"""
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')