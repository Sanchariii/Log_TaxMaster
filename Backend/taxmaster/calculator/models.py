from django.db import models
from django.contrib.auth.models import User



class UserInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inputs", default=8)
    age_group = models.IntegerField()
    annual_income = models.FloatField()
    standard_deduction = models.FloatField()
    other_deductions = models.FloatField()
    deduction_80c = models.FloatField(default=0)
    deduction_80ccd1b = models.FloatField(default=0)
    deduction_80d = models.FloatField(default=0)
    deduction_80e = models.FloatField(default=0)
    deduction_80eea = models.FloatField(default=0)
    deduction_80g = models.FloatField(default=0)
    
def __str__(self):
    return f"User Input - Age Group: {self.age_group}, Income: {self.annual_income}"



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





class TaxResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calculations", default=8)
    user_input = models.ForeignKey(UserInput, on_delete=models.CASCADE, related_name="calculations")
    old_regime_tax = models.DecimalField(max_digits=10, decimal_places=2)
    new_regime_tax = models.DecimalField(max_digits=10, decimal_places=2)
    best_regime = models.CharField(max_length=20)

    def __str__(self):
        return f"Tax Calculation for {self.user.username} on {self.calculated_at}"


