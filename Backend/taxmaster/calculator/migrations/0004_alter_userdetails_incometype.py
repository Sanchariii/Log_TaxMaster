# Generated by Django 5.0.9 on 2024-10-06 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_userdetails_incometype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='incometype',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
