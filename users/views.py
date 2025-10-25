from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
