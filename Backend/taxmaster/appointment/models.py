from django.conf import settings
from django.db import models
from calculator.models import UserRequest
from django.contrib.auth.models import User

class Appointment(models.Model):
    user_request = models.ForeignKey(
        'calculator.UserRequest', 
        on_delete=models.CASCADE, 
        related_name="user_request_appointments",  # Unique related_name,
        null = True
    )
    tax_advisor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="tax_advisor_appointments"  # Unique related_name
    )
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
