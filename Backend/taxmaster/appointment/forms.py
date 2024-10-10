from django import forms
from .models import Appointment
from django.contrib.auth.models import User


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['tax_advisor', 'appointment_date', 'notes']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AvailabilityCheckForm(forms.Form):
    advisor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Tax Advisor'),  # Filter users in the "Tax Advisor" group
        label="Select Tax Advisor"
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Select Date"
    )


class AppointmentRequestForm(forms.ModelForm):
    requested_date = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}), 
        label='Requested Appointment Date'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label='Additional Notes (Optional)'
    )

    class Meta:
        model = Appointment
        fields = ['requested_date', 'notes'] 
