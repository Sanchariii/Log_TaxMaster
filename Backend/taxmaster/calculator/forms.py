from django import forms
from .models import UserDetails, UserDetails, TaxScheme, SurchargeRate

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['age', 'income', 'deductions', 'month']

class SurchargeForm(forms.Form):
    income = forms.FloatField(label='Income')
    
