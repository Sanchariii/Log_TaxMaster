# Generated by Django 5.1.1 on 2024-10-09 18:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_appointment_confirmed_alter_appointment_tax_advisor_and_more'),
        ('calculator', '0008_delete_appointment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='month',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserRequest',
        ),
    ]