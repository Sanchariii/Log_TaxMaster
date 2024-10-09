from django import forms
from .models import UserDetails, UserDetails, TaxScheme, SurchargeRate, TaxDetail

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['age', 'income', 'deductions']

class SurchargeForm(forms.Form):
    income = forms.FloatField(label='Income')
    

class TaxDetailForm(forms.ModelForm):
    class Meta:
        model = TaxDetail
        fields = ['income', 'deductions', 'month']