# Generated by Django 5.1.1 on 2024-10-10 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0009_userdetails_month_alter_userdetails_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxCalculator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Income')),
                ('deductions', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Deductions')),
                ('regime', models.CharField(choices=[('old', 'Old Regime'), ('new', 'New Regime')], max_length=3, verbose_name='Tax Regime')),
            ],
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='deductions',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='income',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='month',
        ),
    ]