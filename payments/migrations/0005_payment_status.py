# Generated by Django 5.0.1 on 2024-02-02 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_alter_payment_cancel_alter_payment_failure_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('success', 'success'), ('cancel', 'cancel'), ('failure', 'PayPal')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
