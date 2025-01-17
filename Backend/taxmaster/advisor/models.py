from django.db import models
from django.contrib.auth.models import User


class UserRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    tax_advisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="advisor_requests")
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    slot = models.CharField(max_length=100, null=True)  # Store the time slot as a string (can use choices)
    date = models.DateField(null=True)  # Store the appointment date
    meeting_type = models.CharField(max_length=20, choices=[('in_person', 'In Person'), ('online_meeting', 'Online Meeting')])

    def __str__(self):
        return f"{self.first_name} {self.last_name} to {self.tax_advisor.username}"
    
    

class TaxAdvisorProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('not_specified', 'Prefer not to specify'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    license_serial = models.CharField(max_length=100, unique=True)
    years_of_experience = models.PositiveIntegerField()
    gender = models.CharField(max_length=30,choices=GENDER_CHOICES, default='Not specified')
    clients_attended_successfully = models.IntegerField(default=0)
    clients_currently_attending = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - License: {self.license_serial}"
