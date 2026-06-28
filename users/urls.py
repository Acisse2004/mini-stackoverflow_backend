from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, LogoutView, ProfileView, MeView
from .google_auth import GoogleLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='login'),
    path('logout/',   LogoutView.as_view(),   name='logout'),
    path('refresh/',  TokenRefreshView.as_view(), name='token_refresh'),
    path('me/',       MeView.as_view(),       name='me'),
    path('google/',   GoogleLoginView.as_view(), name='google-login'),
    path('users/<int:pk>/', ProfileView.as_view(), name='user-profile'),
]