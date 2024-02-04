from django.db import models
from django.utils.translation import gettext_lazy as _

class TransactionAnalytics(models.Model):
    
    transaction_id = models.CharField(max_length=255, unique=True)
    
    status = models.CharField(max_length=50)
    
    transaction_type = models.CharField(max_length=50)
   
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    currency = models.CharField(max_length=3)
   
    payment_method = models.CharField(max_length=50)

    country = models.CharField(max_length=50)
   
    transaction_date = models.DateTimeField()
    
    customer_id = models.CharField(max_length=255)
  
    customer_email = models.EmailField()
    
    product_id = models.CharField(max_length=255, blank=True, null=True)
    
    metadata = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Transaction Analytics")
        verbose_name_plural = _("Transactions Analytics")

    def __str__(self):
        return f"Analytics for Transaction {self.transaction_id}"

class PerformanceReport(models.Model):
   
    report_date = models.DateField()
    
    total_transactions = models.IntegerField()
   
    successful_transactions = models.IntegerField()
   
    failed_transactions = models.IntegerField()
 
    pending_transactions = models.IntegerField()

    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
 
    revenue_by_currency = models.JSONField()

    average_transaction_value = models.DecimalField(max_digits=10, decimal_places=2)

    new_customers = models.IntegerField()
  
    total_customers = models.IntegerField()
  
    total_refunds = models.DecimalField(max_digits=10, decimal_places=2)
   

    class Meta:
        verbose_name = _("Performance Report")
        verbose_name_plural = _("Performance Reports")

    def __str__(self):
        return f"Performance Report for {self.report_date}"
