# Generated by Django 5.0.1 on 2024-02-01 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_creditcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='encrypted_card_number',
            field=models.BinaryField(),
        ),
    ]
