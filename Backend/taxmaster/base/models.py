from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    age = models.IntegerField()
    incometype = models.CharField(max_length=255, null = True)

    def __str__(self):

        return self.user.username if self.user else "No User"

    
    class Meta:
        verbose_name_plural = "User Details"
