from django import forms
# from .models import TaxScheme, SurchargeRate, TaxCalculator
    
class TaxCalculatorForm(forms.Form):
   AGE_GROUP_CHOICES = [
       (1, 'Below 60 years'),
       (2, 'Between 60 and 80 years'),
       (3, 'Above 80 years'),
   ]
   age_group = forms.ChoiceField(choices=AGE_GROUP_CHOICES)
   annual_income = forms.FloatField(label='Annual Income')
   standard_deduction = forms.FloatField(label='Standard Deduction')
   other_deductions = forms.FloatField(label='Other Deductions')