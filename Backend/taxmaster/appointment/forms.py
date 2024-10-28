from django import forms
from .models import Appointment
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time, timedelta,date
from django.core.exceptions import ValidationError

class AppointmentForm(forms.ModelForm):
    SLOT_CHOICES = [
        ('morning', 'Morning (9:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:30 PM - 3:30 PM)'),
        ('evening', 'Evening (4:00 PM - 6:00 PM)'),
    ]

    today = timezone.now().date()
    one_year_from_now = today + timedelta(days=365)

    requested_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control',
            'min': today.strftime('%Y-%m-%d'),
            'max': one_year_from_now.strftime('%Y-%m-%d')
        }),  # Ensure correct date input type
        label='Requested Appointment Date',
        input_formats=['%Y-%m-%d']  # Ensure the date format is correct
    )

    slot = forms.ChoiceField(
        choices=SLOT_CHOICES, 
        widget=forms.RadioSelect,  # Use radio buttons for slot selection
        label="Select Time Slot"
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Select Specific Time"
    )

    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter any additional notes'}),
        required=False,
        label='Additional Notes (Optional)'
    )

    class Meta:
        model = Appointment
        fields = ['requested_date', 'slot', 'time', 'notes']
    
    def clean_appointment_date(self):
       appointment_date = self.cleaned_data.get('appointment_date')
       if appointment_date >= date(2026, 1, 1):
           raise ValidationError("Appointments cannot be booked for dates in or after the year 2026.")
       return appointment_date
        
    def clean_requested_date(self):
        requested_date = self.cleaned_data.get('requested_date')
        today = timezone.now().date()
        one_year_from_now = today + timedelta(days=365)

        if requested_date > one_year_from_now:
            raise forms.ValidationError(f"Date must not be more than one year from today ({one_year_from_now}).")

        return requested_date

    def clean_time(self):
        selected_slot = self.cleaned_data.get('slot')
        selected_time = self.cleaned_data.get('time')

        slot_time_ranges = {
            'morning': (time(9, 0), time(12, 0)),
            'afternoon': (time(12, 30), time(15, 30)),
            'evening': (time(16, 0), time(18, 0)),
        }

        if selected_slot and selected_time:
            start_time, end_time = slot_time_ranges[selected_slot]
            if not (start_time <= selected_time <= end_time):
                raise forms.ValidationError(f"The selected time {selected_time} is not within the {selected_slot} slot range ({start_time} - {end_time}).")

        return selected_time

class AvailabilityCheckForm(forms.Form):
    advisor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Tax Advisor'),  # Filter users in the "Tax Advisor" group
        label="Select Tax Advisor"
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Only a date input, no time
        label="Select Date"
    )
    def clean_date(self):
       date = self.cleaned_data.get('date')
       if date >= date(2026, 1, 1):
           raise ValidationError("Appointments cannot be checked for dates in or after the year 2026.")
       return date

class AppointmentRequestForm(forms.ModelForm):

    SLOT_CHOICES = [
        ('morning', 'Morning (9:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:30 PM - 3:30 PM)'),
        ('evening', 'Evening (4:00 PM - 6:00 PM)'),
    ]

    MEETING_TYPE_CHOICES = [
        ('in_person', 'In Person'),
        ('online', 'Online'),
    ]
    

    requested_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Ensure correct date input type
        label='Requested Appointment Date',
        input_formats=['%Y-%m-%d']  # Ensure the date format is correct
    )
    
    slot = forms.ChoiceField(
        choices=SLOT_CHOICES, 
        widget=forms.RadioSelect(),  # Use radio buttons for slot selection
        label="Select Time Slot"
    )
    
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Select Specific Time"
    )

    meeting_type = forms.ChoiceField(
        choices=MEETING_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Meeting Type"
    )
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4,'cols':40, 'placeholder': 'Enter any additional notes'}),
        required=False,
        label='Additional Notes (Optional)'
    )

    class Meta:
        model = Appointment
        fields = ['requested_date', 'slot', 'time', 'notes']
        
    def clean_requested_date(self):
        requested_date = self.cleaned_data.get('requested_date')
        today = timezone.now().date()

        if requested_date < today:
            raise forms.ValidationError("You cannot select a past date for the appointment.")
        
        return requested_date

    def clean_time(self):
        selected_slot = self.cleaned_data.get('slot')
        selected_time = self.cleaned_data.get('time')

        slot_time_ranges = {
            'morning': (time(9, 0), time(12, 0)),
            'afternoon': (time(12, 30), time(15, 30)),
            'evening': (time(16, 0), time(18, 0)),
        }

        if selected_slot and selected_time:
            start_time, end_time = slot_time_ranges[selected_slot]
            if not (start_time <= selected_time <= end_time):
                raise forms.ValidationError(f"The selected time {selected_time} is not within the {selected_slot} slot range ({start_time} - {end_time}).")

        return selected_time
