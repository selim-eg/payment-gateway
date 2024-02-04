from django.urls import path
from .views import WebhookEndpointListCreateAPIView, WebhookEndpointRetrieveUpdateDestroyAPIView
app_name = "webhooks"
urlpatterns = [
    path('', WebhookEndpointListCreateAPIView.as_view(), name='webhook-list-create'),
    path('<int:pk>/', WebhookEndpointRetrieveUpdateDestroyAPIView.as_view(), name='webhook-retrieve-update-destroy'),
]
