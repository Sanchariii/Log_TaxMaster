# Generated by Django 5.1.1 on 2024-10-09 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
        ('calculator', '0008_delete_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='user_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_request_appointments', to='calculator.userrequest'),
        ),
    ]