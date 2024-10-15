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
   deduction_80c = forms.FloatField(label='80C Deductions (Investments in PPF, ELSS, NSC, etc.)', required=False)
   deduction_80d = forms.FloatField(label='80D Deductions (Health Insurance Premiums)', required=False)
   deduction_80e = forms.FloatField(label='80E Deductions (Education Loan Interest)', required=False)
   deduction_80eea = forms.FloatField(label='80EEA Deductions (Home Loan Interest)', required=False)
   deduction_80g = forms.FloatField(label='80G Deductions (Charitable Donations)', required=False)