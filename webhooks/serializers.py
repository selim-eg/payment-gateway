from rest_framework import serializers
from .models import WebhookEndpoint

class WebhookEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')
