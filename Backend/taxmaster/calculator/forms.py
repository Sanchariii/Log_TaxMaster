from django import forms
from .models import TaxScheme, SurchargeRate, TaxCalculator
    
class TaxCalculatorForm(forms.ModelForm):
    class Meta:
        model = TaxCalculator
        fields = ['income', 'deductions']
        labels = {
            'income': 'Income',
            'deductions': 'Deductions',
        }
