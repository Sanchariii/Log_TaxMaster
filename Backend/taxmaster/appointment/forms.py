from django import forms
from .models import Appointment
from django.contrib.auth.models import User
from django.utils import timezone



class AppointmentForm(forms.ModelForm):
    SLOT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    slot = forms.ChoiceField(
        choices=SLOT_CHOICES, 
        widget=forms.RadioSelect,  # Use radio buttons for slot selection
        label="Select Time Slot"
    )

    class Meta:
        model = Appointment
        fields = ['tax_advisor', 'appointment_date', 'slot', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),  # Only a date input, no time
        }

class AvailabilityCheckForm(forms.Form):
    advisor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Tax Advisor'),  # Filter users in the "Tax Advisor" group
        label="Select Tax Advisor"
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Only a date input, no time
        label="Select Date"
    )

class AppointmentRequestForm(forms.ModelForm):
    
    SLOT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    
    requested_date = forms.DateField(
        widget=forms.SelectDateWidget(),  # Only show dates, no time
        label='Requested Appointment Date'
    )
    slot = forms.ChoiceField(
        choices=SLOT_CHOICES, 
        widget=forms.RadioSelect,  # Use radio buttons for slot selection
        label="Select Time Slot"
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label='Additional Notes (Optional)'
    )

    class Meta:
        model = Appointment
        fields = ['requested_date', 'notes']
        
    def clean_requested_date(self):
        requested_date = self.cleaned_data.get('requested_date')
        today = timezone.now().date()

        if requested_date < today:
            raise forms.ValidationError("You cannot select a past date for the appointment.")
        
        return requested_date
