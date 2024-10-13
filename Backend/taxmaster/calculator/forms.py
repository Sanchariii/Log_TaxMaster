from django import forms
from .models import TaxScheme, SurchargeRate, TaxCalculator
    
class TaxCalculatorForm(forms.ModelForm):
    class Meta:
        model = TaxCalculator
        fields = ['income_type', 'age_group', 'total_income','net_income', 'deductions']
        labels = {
            'income_type': 'Type of Income',
            # 'regime': 'Tax Regime',
            'age_group': 'Age Group',
            'total_income': 'Total Income',
            'net_income': 'Net Income(for Business Income)',
            'deductions': 'Deductions',
        }
