# Generated by Django 5.1.4 on 2025-05-29 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_tournamentregistration_partner_2_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentregistration',
            name='partner_2_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
