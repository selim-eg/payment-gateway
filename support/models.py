from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid

class SupportTicket(models.Model):
    # id = models.UUIDField(primary_key=True , default=uuid.uuid4, editable=False, unique=True)
    STATUS_CHOICES = [
        ('open', _('Open')),
        ('in_progress', _('In Progress')),
        ('resolved', _('Resolved')),
        ('closed', _('Closed')),
    ]

    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]

    # ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    attachment = models.FileField(upload_to='support_attachments/', null=True, blank=True)

    class Meta:
        verbose_name = _('Support Ticket')
        verbose_name_plural = _('Support Tickets')

    def __str__(self):
        return f"Ticket #{self.ticket_id} - {self.subject}"

class TicketResponse(models.Model):
    # id = models.UUIDField(primary_key=True , default=uuid.uuid4, editable=False, unique=True)
    # response_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    internal_note = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='response_attachments/', null=True, blank=True)

    class Meta:
        verbose_name = _('Ticket Response')
        verbose_name_plural = _('Ticket Responses')

    def __str__(self):
        return f"Response #{self.response_id} by {self.user.username} for Ticket #{self.ticket.ticket_id}"

