# Generated by Django 5.0.1 on 2024-01-31 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=255)),
                ('object_id', models.CharField(max_length=255)),
                ('object_repr', models.CharField(max_length=255)),
                ('action_time', models.DateTimeField(auto_now_add=True)),
                ('changes', models.TextField()),
                ('remote_address', models.GenericIPAddressField()),
                ('additional_data', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Audit Log',
                'verbose_name_plural': 'Audit Logs',
            },
        ),
        migrations.CreateModel(
            name='ComplianceDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=50)),
                ('issue_date', models.DateField()),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('document_number', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='compliance_documents/')),
                ('verified', models.BooleanField(default=False)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compliance_documents', to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verified_compliance_documents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Compliance Document',
                'verbose_name_plural': 'Compliance Documents',
            },
        ),
        migrations.CreateModel(
            name='SecurityEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('login_attempt', 'Login Attempt'), ('password_change', 'Password Change'), ('unauthorized_access', 'Unauthorized Access'), ('data_export', 'Data Export')], max_length=50)),
                ('description', models.TextField()),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.CharField(max_length=255)),
                ('occurred_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=50)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('additional_info', models.JSONField(blank=True, null=True)),
                ('resolved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_security_events', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='security_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Security Event',
                'verbose_name_plural': 'Security Events',
            },
        ),
    ]
