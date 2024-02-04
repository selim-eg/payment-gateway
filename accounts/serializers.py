from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import (
    AuthenticationFailed,
    JWTAuthentication,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


    
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['username'],
            username=validated_data['username'],
            password=validated_data['password']
        )
       
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        refresh_token = TokenObtainPairSerializer.get_token(user=instance)
        data["refresh_token"] = str(refresh_token)
        data["access_token"] = str(refresh_token.access_token)

        return {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
            "user": {
                "id": instance.id,
                # "first_name": instance.first_name,
                # "last_name": instance.last_name,
                "username": instance.username,
            },
        }


    class Meta:
        model = User
        fields = (
            "id",
            # "first_name",
            # "last_name",
            "username",
            "email",
            "password",

        )
        extra_kwargs = {
            # "first_name": {"required": True},
            # "last_name": {"required": True},
            "email": {"required": True},
        }



class UserLoggedInSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
                    'id', 
                    # 'first_name',
                    # 'last_name', 
                    'username',
                )

class JWTLoginSerializer(TokenObtainPairSerializer,):
    def validate(self, attrs):
        data = super().validate(attrs)
        update_last_login(None, self.user)
        data["user"] = UserLoggedInSerializer(self.user).data
        return data
 