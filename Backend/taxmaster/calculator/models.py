from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    age = models.IntegerField()
    income = models.FloatField()
    deductions = models.FloatField()
    incometype = models.CharField(max_length=255, null = True)
    month = models.DateField(null=True)

    def __str__(self):

        return self.user.username if self.user else "No User"


        # return f"{self.user.username}'s tax details for {self.month.strftime('%B %Y')}"

    
    class Meta:
        verbose_name_plural = "User Details"

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
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
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






