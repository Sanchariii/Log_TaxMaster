# Generated by Django 5.0.9 on 2024-11-11 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor', '0009_taxadvisorprofile_clients_attended_successfully_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='meeting_type',
            field=models.CharField(choices=[('in_person', 'In Person'), ('online_meeting', 'Online Meeting')], default=0, max_length=20),
            preserve_default=False,
        ),
    ]
