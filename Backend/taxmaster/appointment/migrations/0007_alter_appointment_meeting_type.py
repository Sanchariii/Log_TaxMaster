# Generated by Django 5.1.1 on 2024-11-05 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0006_appointment_meeting_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='meeting_type',
            field=models.CharField(choices=[('in_person', 'In Person'), ('online_meeting', 'Online Meeting')], default='online', max_length=20),
        ),
    ]
