from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):

    code = models.CharField(max_length=50, unique=True)

    name = models.CharField(max_length=255)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    billing_cycle = models.CharField(max_length=50)

    billing_cycle_days = models.IntegerField()

    currency = models.CharField(max_length=3)
  
    is_active = models.BooleanField(default=True)
   
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
 
    usage_limits = models.JSONField()
 
    features = models.JSONField()


class Subscription(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    start_date = models.DateTimeField()
  
    end_date = models.DateTimeField()
   
    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    last_payment_date = models.DateTimeField(null=True, blank=True)

    next_payment_date = models.DateTimeField()

    last_transaction_id = models.CharField(max_length=255, blank=True, null=True)
 
    next_transaction_id = models.CharField(max_length=255, blank=True, null=True)



