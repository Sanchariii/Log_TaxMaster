from django.contrib import admin
from .models import UserDetails, TaxScheme, SurchargeRate, TaxCalculation

# Register your models here
admin.site.register(UserDetails)
admin.site.register(TaxScheme)
admin.site.register(SurchargeRate)
admin.site.register(TaxCalculation)
