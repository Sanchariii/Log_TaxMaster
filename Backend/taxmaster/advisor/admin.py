from django.contrib import admin
from .models import UserRequest, TaxAdvisorProfile

# Register your models here.
admin.site.register(UserRequest)
admin.site.register(TaxAdvisorProfile)
