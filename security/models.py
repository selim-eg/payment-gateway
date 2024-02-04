from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class SecurityEvent(models.Model):
    EVENT_TYPES = [
        ('login_attempt', _('Login Attempt')),
        ('password_change', _('Password Change')),
        ('unauthorized_access', _('Unauthorized Access')),
        ('data_export', _('Data Export')),
       
    ]

   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    occurred_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resolved_security_events')
    resolved_at = models.DateTimeField(null=True, blank=True)
    additional_info = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = _('Security Event')
        verbose_name_plural = _('Security Events')

    def __str__(self):
        return f"Security Event #{self.event_id} - {self.event_type}"

class AuditLog(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    object_id = models.CharField(max_length=255)
    object_repr = models.CharField(max_length=255)
    action_time = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()
    remote_address = models.GenericIPAddressField()
    additional_data = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')

    def __str__(self):
        return f"Audit Log #{self.log_id} - {self.action}"

class ComplianceDocument(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compliance_documents')
    document_type = models.CharField(max_length=50)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    document_number = models.CharField(max_length=255)
    file = models.FileField(upload_to='compliance_documents/')
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='verified_compliance_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('Compliance Document')
        verbose_name_plural = _('Compliance Documents')

    def __str__(self):
        return f"Compliance Document #{self.document_id} - {self.document_type}"


