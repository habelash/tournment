# Generated by Django 5.1.4 on 2025-05-25 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournamentregistration',
            name='registered_at',
        ),
        migrations.AddField(
            model_name='tournamentregistration',
            name='payment_status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
