# Generated by Django 5.0.1 on 2024-02-02 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='cancel',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='failure',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='success',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
