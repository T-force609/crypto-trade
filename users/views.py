from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, AdminTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django_countries import countries
from rest_framework_simplejwt.views import TokenObtainPairView

#User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CountryListView(APIView):
    def get(self, request):
        country_list = [{'code': code, 'name': name} for code, name in countries]
        return Response(country_list)
    
class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer