from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    tax_advisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="advisor_requests")
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} to {self.tax_advisor.username}"