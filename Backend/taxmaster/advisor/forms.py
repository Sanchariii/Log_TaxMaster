from django import forms
from .models import TaxAdvisorProfile

class TaxAdvisorProfileForm(forms.ModelForm):
    class Meta:
        model = TaxAdvisorProfile
        fields = ['license_serial', 'years_of_experience','gender']
        widgets = {
            'license_serial': forms.TextInput(attrs={'placeholder': 'License Serial'}),
            'years_of_experience': forms.NumberInput(attrs={'placeholder': 'Years of Experience'}),
            'gender': forms.Select(choices=TaxAdvisorProfile.GENDER_CHOICES),
            }

    def clean(self):
        cleaned_data = super().clean()
        license_serial = cleaned_data.get('license_serial')
        years_of_experience = cleaned_data.get('years_of_experience')

        if not license_serial:
            raise forms.ValidationError("License Serial is required.")

        if not years_of_experience:
            raise forms.ValidationError("Years of Experience are required.")
        
        if years_of_experience > 50:
            raise forms.ValidationError("Years of Experience cannot exceed 50 years.")

        return cleaned_data
