from django.db import models
from django.utils.translation import gettext_lazy as _
from orders.models import Order
import uuid


class Customer(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    

    def __str__(self):
        return self.user.username

class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=3, default='USD')
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(max_length=50, choices=[('checking', 'Checking'), ('savings', 'Savings')])
    

    def __str__(self):
        return f"{self.account_number} - {self.customer.user.username}"

class PaymentMethod(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payment_methods')
    type = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('paypal', 'PayPal')])
    details = models.JSONField()  # This field can store card number, expiry date, etc., in an encrypted format
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.type} - {self.customer.user.username}"





class Payment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount_cents = models.DecimalField(max_digits=12, decimal_places=2)
    expiration = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    billing_data = models.JSONField()  
    currency = models.CharField(max_length=3)
    integration_id = models.IntegerField()
    lock_order_when_paid = models.BooleanField(default=False)
    payment_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    success = models.CharField(max_length=500)
    cancel = models.CharField(max_length=500)
    failure = models.CharField(max_length=500)


    def __str__(self):
        return f"Payment {self.payment_token} for Order {self.order_id}"


class Transaction(models.Model):
    # account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL ,null=True,blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, related_name='payment')
    order =  models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, related_name='order')
    transaction_type = models.CharField(max_length=50, choices=[('charge', 'Charge'), ('refund', 'Refund'), ('withdrawal', 'Withdrawal')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=50, choices=[('refund','Refund'),('cancel', 'Cancel'), ('paid', 'Paid'), ('failed', 'Failed') ,('refund','Refund')])
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return f"Transaction {self.id} - {self.user}"