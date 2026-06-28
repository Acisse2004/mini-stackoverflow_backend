import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserProfileSerializer

@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token manquant.'}, status=status.HTTP_400_BAD_REQUEST)

        google_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
        google_response = requests.get(google_url)

        if google_response.status_code != 200:
            return Response({'error': 'Token Google invalide.'}, status=status.HTTP_400_BAD_REQUEST)

        google_data = google_response.json()
        email = google_data.get('email')
        name = google_data.get('name', '')
        picture = google_data.get('picture', '')

        if not email:
            return Response({'error': 'Email manquant.'}, status=status.HTTP_400_BAD_REQUEST)

        username = email.split('@')[0]
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })