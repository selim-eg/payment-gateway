from django.shortcuts import render
from rest_framework import generics
from .models import WebhookEndpoint
from .serializers import WebhookEndpointSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

class WebhookEndpointListCreateAPIView(generics.ListCreateAPIView):
    """
    get:
    Webhooks List.

    These cards can be used to test payment transactions in the application.

    | Name           | NUMBER            | CVC         | DATE            | Status
    |-----------------|-------------------|-------------|-----------------|-------
    | mohamed selim   | 4242424242424242  | 123         | 01 / 25         | success
    | omar ahmed      | 4000056655665556  | 456         | 02 / 26         | cancel
    | khaled said     | 4343434343434343  | 789         | 03 / 27         | failure
    
    """
    queryset = WebhookEndpoint.objects.all()
    serializer_class = WebhookEndpointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WebhookEndpoint.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WebhookEndpointRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = WebhookEndpointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return WebhookEndpoint.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        
        webhook = self.get_object()
        if webhook.user != self.request.user:
            raise PermissionDenied('You do not have permission to edit this WebhookEndpoint.')
        serializer.save()

    def perform_destroy(self, instance):
        
        if instance.user != self.request.user:
            raise PermissionDenied('You do not have permission to delete this WebhookEndpoint.')
        instance.delete()

    def perform_patch(self, serializer,):
        webhook = self.get_object()
        if webhook.user != self.request.user:
            raise PermissionDenied('You do not have permission to edit this WebhookEndpoint.')
        serializer.save()