from django.db import models
from django.utils.translation import gettext_lazy as _

class IdentityVerification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='identity_verifications')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    identification_type = models.CharField(max_length=50, choices=[('passport', 'Passport'), ('id_card', 'ID Card'), ('driver_license', 'Driver License')])
    identification_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    country_of_issue = models.CharField(max_length=50)
    verification_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    document_image = models.ImageField(upload_to='identity_documents/')
    

    def __str__(self):
        return f"{self.user.username} - {self.verification_status}"

class ComplianceReport(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='compliance_reports')
    report_type = models.CharField(max_length=50, choices=[('kyc', 'KYC'), ('aml', 'AML'), ('sars', 'SARs')])
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('submitted', 'Submitted'), ('reviewed', 'Reviewed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = models.TextField()
    resolution = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='reviewed_compliance_reports')
    

    def __str__(self):
        return f"{self.user.username} - {self.report_type} - {self.status}"

