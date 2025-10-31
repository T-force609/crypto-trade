from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    country = CountryField(name_only=True) 

    class Meta:
        model = User
        fields = [
            "username", "email", "password", "password_confirmation",
            "first_name", "last_name", "country"
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        # allow only staff or superuser — adjust condition if you want only superusers
        if not (user.is_staff or user.is_superuser):
            raise serializers.ValidationError("Admin credentials required.")
        return data