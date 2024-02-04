from django.db import models
from django.utils.translation import gettext_lazy as _
# from django_cryptography.fields import encrypt
from cryptography.fernet import Fernet,InvalidToken
from django.conf import settings
import os


class Account(models.Model):
    
    account_number = models.CharField(max_length=20, unique=True, verbose_name=_("Account Number"))
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_("User"))
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Balance"))
    currency = models.CharField(max_length=3, verbose_name=_("Currency"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    overdraft_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Overdraft Limit"))
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_("Interest Rate"))
    account_type = models.CharField(max_length=50, choices=[('S', 'Savings'), ('C', 'Checking')], verbose_name=_("Account Type"))

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"

class Transaction(models.Model):
    
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name=_("Transaction ID"))
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', verbose_name=_("Account"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    transaction_type = models.CharField(max_length=50, choices=[('D', 'Deposit'), ('W', 'Withdrawal')], verbose_name=_("Transaction Type"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    status = models.CharField(max_length=50, choices=[('P', 'Pending'), ('C', 'Completed'), ('F', 'Failed')], default='P', verbose_name=_("Status"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    destination_account = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Destination Account"))
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Fee"))
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=1, verbose_name=_("Exchange Rate"))
    reference = models.CharField(max_length=100, blank=True, verbose_name=_("Reference"))

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        return f"{self.transaction_id} - {self.account.account_number}"




fernet_key = os.environ.get('FERNET_KEY', settings.FERNET_KEY)
# fernet_key =  "xh8Vhq1FB9ISCPagte4E-TkxWdrlUUtkBhZnX2U6hCk="
cipher_suite = Fernet(fernet_key)

class CreditCard(models.Model):
    card_number = models.CharField(max_length=500)  
    card_expiry = models.CharField(max_length=500)
    cardholder_name = models.CharField(max_length=500)
    card_cvv = models.CharField(max_length=500)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_card_info(self, card_number , card_expiry,cardholder_name,card_cvv):
       
        self.card_number = cipher_suite.encrypt(card_number.encode('utf-8')).decode('utf-8')
        self.card_expiry = cipher_suite.encrypt(card_expiry.encode('utf-8')).decode('utf-8')
        self.cardholder_name = cipher_suite.encrypt(cardholder_name.encode('utf-8')).decode('utf-8')
        self.card_cvv = cipher_suite.encrypt(card_cvv.encode('utf-8')).decode('utf-8')

    def get_card_info(self):
        
        card_info = { 
                "card_number": cipher_suite.decrypt(self.card_number).decode('utf-8'),
                "card_expiry": cipher_suite.decrypt(self.card_expiry).decode('utf-8'),
                "cardholder_name": cipher_suite.decrypt(self.cardholder_name).decode('utf-8'),
                "card_cvv": cipher_suite.decrypt(self.card_cvv).decode('utf-8'),
            }
        return card_info
    
    def save(self, *args, **kwargs):
        # if not self.card_number and  not self.card_number.startswith('gAAAAA'):
        self.set_card_info(self.card_number , self.card_expiry,self.cardholder_name,self.card_cvv)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_card_info()}"