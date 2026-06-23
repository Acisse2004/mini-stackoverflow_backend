from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer


def post(self, request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response({'error': 'Question introuvable.'}, status=status.HTTP_404_NOT_FOUND)
    
    # ✅ Ajoute ces 3 lignes ici
    if request.user == question.author:
        return Response({'error': 'Vous ne pouvez pas voter pour votre propre question.'}, status=status.HTTP_403_FORBIDDEN)

    value = request.data.get('value')
    # ... reste du code


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    US001 — Inscription
    """
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Générer les tokens JWT directement après inscription
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    POST /api/auth/login/
    US002 — Connexion
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    US002 — Déconnexion (blacklist le refresh token)
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Déconnexion réussie.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': 'Token invalide.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/users/<id>/   — Voir un profil (US003)
    PUT  /api/users/<id>/   — Modifier son profil
    US003, US014
    """
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        # Un user ne peut modifier que son propre profil
        instance = self.get_object()
        if instance != request.user:
            return Response({'error': 'Non autorisé.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class MeView(generics.RetrieveAPIView):
    """
    GET /api/auth/me/
    Retourne le profil de l'utilisateur connecté
    """
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
