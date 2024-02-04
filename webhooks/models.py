from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

class WebhookEndpoint(models.Model):
   
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    description = models.CharField(max_length=255)
   
    url = models.URLField(max_length=2048)
    is_test = models.BooleanField(default=True)
    secret = models.CharField(max_length=255)
    
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('disabled', 'Disabled')])
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    # events = models.JSONField(default=list)
    

class WebhookEvent(models.Model):
    
    endpoint = models.ForeignKey(WebhookEndpoint, on_delete=models.CASCADE)
    
    event_type = models.CharField(max_length=255)
   
    data = models.JSONField()
   
    date_occurred = models.DateTimeField()
    
    date_sent = models.DateTimeField(null=True, blank=True)
   
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('failed', 'Failed')])
    
    attempt_count = models.IntegerField(default=0)
    
    response_status = models.CharField(max_length=10, blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
