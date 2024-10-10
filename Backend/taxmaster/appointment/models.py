from django.conf import settings
from django.db import models
from advisor.models import UserRequest
from django.contrib.auth.models import User

class Appointment(models.Model):
    user_request = models.ForeignKey(
        UserRequest, 
        on_delete=models.CASCADE, 
        related_name="user_request_appointments",  
        null=True
    )
    tax_advisor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="advisor_appointments"
    )
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment for {self.user_request.user.username} with {self.tax_advisor.username}"
