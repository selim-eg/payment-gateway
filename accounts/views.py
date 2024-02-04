from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (UserCreateSerializer,
                        #    UserLoginSerializer,
                           JWTLoginSerializer)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, UpdateAPIView

User = get_user_model()

class SignupView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = ()
    authentication_classes = ()
    # POST /accounts/register/
    @swagger_auto_schema(
            operation_id="Register a new user",
            operation_description=    """
                                    post:
                                    Register a new user.

                                    Payload example:
                                    {
                                        "username": "newuser",
                                        "email": "newuser@example.com",
                                        "password": "newpassword123"
                                    }
                                    """,
            request_body=UserCreateSerializer,

            description="This endpoint allows users to register a new account", 
            deprecated=False ,

            tags=["Authentication"],  
            # security=[{"Bearer": []}],  
            # summary="Create a new user", 
            # parameters=[
            #     openapi.Parameter("username", openapi.IN_QUERY, description="Username", type=openapi.TYPE_STRING),
            #     openapi.Parameter("password", openapi.IN_QUERY, description="Password", type=openapi.TYPE_STRING)
            # ],
            # consumes=["application/json"], 
            # produces=["application/json"],

            responses={
                200: openapi.Response(
                    description="User logged in successfully",
                    examples={
                        "application/json": {                      
                            "username": "string",
                            "token": "string"
                            
                        }
                    }
                )
            }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class JWTLoginView(TokenObtainPairView):
    serializer_class = JWTLoginSerializer
    # POST /accounts/login/
    @swagger_auto_schema(
            operation_id="Login a user",
            operation_description="""
                                    post:
                                    Login a user.

                                    Payload example:
                                    {
                                        "username": "existinguser",
                                        "password": "userpassword123"
                                    }
                                    """,
            request_body=JWTLoginSerializer,
            tags=["Authentication"],  
            # responses={200: UserLoginResponseSerializer},
            responses={
                200: openapi.Response(
                    description="User logged in successfully",
                    examples={
                        "application/json": {
                            "username": "existinguser",
                            "token": "token_value"
                        }
                    }
                )
            }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

