from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
# from base.models import UserDetails



class UserInput(models.Model):
   age_group = models.IntegerField()
   annual_income = models.FloatField()
   standard_deduction = models.FloatField()
   other_deductions = models.FloatField()
   def __str__(self):
       return f"User Input - Age Group: {self.age_group}, Income: {self.annual_income}"

# class TaxCalculator(models.Model):
#     INCOME_TYPE_CHOICES=[
#         ('salarised', 'Salarised'),
#         ('business', 'Business'),]
        
#     # REGIME_CHOICES = [
#     #     ('old', 'Old Regime'),
#     #     ('new', 'New Regime'),
#     # ]

#     AGE_CHOICES = [
#         ('below_60', 'Below_60'),
#         ('senior', '60 to 80'),
#         ('super_senior', 'Above 80'),
#     ]
#     # user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
#     income_type = models.CharField(max_length=10, choices=INCOME_TYPE_CHOICES, verbose_name='Income Type', null=True)
#     # regime = models.CharField(max_length=10, choices=REGIME_CHOICES, verbose_name='Tax Regime', null=True)
#     age_group = models.CharField(max_length=12, choices=AGE_CHOICES, verbose_name='Age Group', null=True)
#     total_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total Income', null=True)
#     user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
#     income_type = models.CharField(max_length=10, choices=INCOME_TYPE_CHOICES, verbose_name='Income Type')
#     #regime = models.CharField(max_length=10, choices=REGIME_CHOICES, verbose_name='Tax Regime')
#     age_group = models.CharField(max_length=12, choices=AGE_CHOICES, verbose_name='Age Group')
#     total_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total Income')
#     net_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Net Income after Expenses', null=True, blank=True)
#     income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Income', null=True)
#     deductions = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Deductions', default=0)

#     def __str__(self):
#         return f"{self.user_details.user.username} ({self.get_income_type_display()})"

class TaxScheme(models.Model):
    regime = models.CharField(max_length=10)  # 'old' or 'new'
    slab = models.CharField(max_length=50)
    rate = models.FloatField()

    def __str__(self):
        return f"{self.regime} - {self.slab}"

class SurchargeRate(models.Model):
    slab = models.CharField(max_length=50)
    rate = models.FloatField()

    def __str__(self):
        return self.slab
    
    
class TaxCalculation(models.Model):
    # user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    old_regime_tax = models.FloatField()
    new_regime_tax = models.FloatField()
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tax Calculation for {self.user_details.user.username} on {self.calculated_at}"

def update_details_fields(sender, instance, created, **kwargs):
    if created:
        if instance.user:
            # You can perform actions here that depend on the user
            print(f"User: {instance.user.username}")
        else:
            # Handle the case where user is None
            print("UserDetails instance has no associated user.")








