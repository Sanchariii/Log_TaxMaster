# Generated by Django 5.1.1 on 2024-10-09 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0007_userrequest_appointment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]