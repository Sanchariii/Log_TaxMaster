from django import forms
from .models import TaxScheme, SurchargeRate, TaxCalculator
    
class TaxCalculatorForm(forms.ModelForm):
    class Meta:
        model = TaxCalculator
        fields = ['income_type', 'age_group', 'total_income','net_income', 'deductions']
        labels = {
            'income_type': 'Type of Income',
            'age_group': 'Age Group',
            'total_income': 'Total Income',
            'net_income': 'Net Income(for Business Income)',
            'deductions': 'Deductions',
        }
        widgets = {
           'income_type': forms.Select(attrs={'class': 'form-control'}),
           'age_group': forms.Select(attrs={'class': 'form-control'}),
           'total_income': forms.NumberInput(attrs={'class': 'form-control'}),
           
           'net_income': forms.NumberInput(attrs={'class': 'form-control'}),
           'deductions': forms.NumberInput(attrs={'class': 'form-control'}),
       }
