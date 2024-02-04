from django.contrib import admin
from .models import SecurityEvent,AuditLog,ComplianceDocument
# Register your models here.
admin.site.register(SecurityEvent)
admin.site.register(AuditLog)
admin.site.register(ComplianceDocument)