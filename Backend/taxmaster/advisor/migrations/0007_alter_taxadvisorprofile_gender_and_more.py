# Generated by Django 5.0.9 on 2024-10-16 14:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor', '0006_taxadvisorprofile_gender'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxadvisorprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('not_specified', 'Prefer not to specify')], default='Not specified', max_length=30),
        ),
        migrations.AlterField(
            model_name='taxadvisorprofile',
            name='license_serial',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='taxadvisorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]