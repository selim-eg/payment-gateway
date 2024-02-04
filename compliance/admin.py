from django.contrib import admin
from .models import IdentityVerification,ComplianceReport
# Register your models here.
admin.site.register(IdentityVerification)
admin.site.register(ComplianceReport)