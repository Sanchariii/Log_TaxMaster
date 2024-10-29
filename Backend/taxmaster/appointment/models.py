from django.conf import settings
from django.db import models
from advisor.models import UserRequest
from django.contrib.auth.models import User

class Appointment(models.Model):
    
    SLOT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    
    MEETING_TYPE_CHOICES = [
        ('in_person', 'In Person'),
        ('online_meeting', 'Online Meeting'),
    ]

    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="appointments",
        null=True
    )
    
    # user_request = models.ForeignKey(
    #     UserRequest, 
    #     on_delete=models.CASCADE, 
    #     related_name="user_request_appointments",  
    #     null=True
    # )
    tax_advisor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="advisor_appointments"
    )
    appointment_date = models.DateField()
    slot = models.CharField(max_length=10, choices=SLOT_CHOICES, null=True)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE_CHOICES, default='online')
    notes = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment with {self.tax_advisor.username}"
