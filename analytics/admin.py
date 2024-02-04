from django.contrib import admin
from .models import TransactionAnalytics,PerformanceReport
# Register your models here.
admin.site.register(TransactionAnalytics)
admin.site.register(PerformanceReport)