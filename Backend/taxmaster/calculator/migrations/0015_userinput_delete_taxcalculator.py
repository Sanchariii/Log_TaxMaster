# Generated by Django 5.0.9 on 2024-10-14 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0014_remove_taxcalculator_regime'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_group', models.IntegerField()),
                ('annual_income', models.FloatField()),
                ('standard_deduction', models.FloatField()),
                ('other_deductions', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='TaxCalculator',
        ),
    ]
