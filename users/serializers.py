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
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Identifiants incorrects.')
        if not user.is_active:
            raise serializers.ValidationError('Compte désactivé.')
        data['user'] = user
        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
    """US003, US014 — Profil + statistiques"""
    question_count = serializers.ReadOnlyField()
    answer_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'bio', 'avatar',
            'question_count', 'answer_count', 'date_joined'
        )
        read_only_fields = ('id', 'date_joined')


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializer léger utilisé dans les autres apps"""
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')
