from django.urls import path
from .views import (
                SignupView,
                JWTLoginView
                )

app_name = 'accounts'

urlpatterns = [
    path('register/', SignupView.as_view(), name='register'),
    path("login/", JWTLoginView.as_view()),
]
