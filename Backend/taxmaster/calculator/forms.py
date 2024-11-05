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
    deduction_80c = forms.FloatField(label='80C Deductions (Investments in PPF, EPF, NSC,SCSS etc.)', required=False)
    deduction_80ccd1b = forms.FloatField(label='80CCD(1B) Deductions (NPS)', required=False)
    deduction_80d = forms.FloatField(label='80D Deductions (Health Insurance Premium)', required=False)
    deduction_80e = forms.FloatField(label='80E Deductions (Education Loan Interest)', required=False)
    deduction_80eea = forms.FloatField(label='80EEA Deductions (Home Loan Interest)', required=False)
    deduction_80g = forms.FloatField(label='80G Deductions (Charitable Donations)', required=False)

    def clean_deduction_80c(self):
        data = self.cleaned_data['deduction_80c']
        if data and data > 150000:
            raise forms.ValidationError("80C deductions cannot exceed ₹1,50,000.")
        return data
    
    def clean_deduction_80ccd1b(self):
        data = self.cleaned_data['deduction_80ccd1b']
        if data and data > 50000:
            raise forms.ValidationError("80CCD(1B) deductions cannot exceed ₹50,000.")
        return data

    def clean_deduction_80d(self):
        data = self.cleaned_data['deduction_80d']
        if data and data > 100000:
            raise forms.ValidationError("80D deductions cannot exceed ₹50,000.")
        return data
    


    def clean_deduction_80e(self):
        data = self.cleaned_data['deduction_80e']
        return data  

    def clean_deduction_80eea(self):
        data = self.cleaned_data['deduction_80eea']
        if data and data > 150000:
            raise forms.ValidationError("80EEA deductions cannot exceed ₹1,50,000.")
        return data

    def clean_deduction_80g(self):
        data = self.cleaned_data['deduction_80g']
        
        if data and data > 100000:
            raise forms.ValidationError("80G deductions cannot exceed ₹1,00,000.")
        return data


