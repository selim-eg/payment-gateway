# Generated by Django 5.0.1 on 2024-02-02 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_testcard_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcard',
            name='status',
            field=models.CharField(choices=[('success', 'success'), ('cancel', 'cancel'), ('failure', 'failure')], max_length=50),
        ),
    ]
