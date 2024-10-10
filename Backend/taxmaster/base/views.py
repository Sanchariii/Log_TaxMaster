from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from appointment.models import Appointment
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import is_User_or_Advisor
from advisor.models import UserRequest
from django.db import models

@login_required
@user_passes_test(is_User_or_Advisor)
def dashboard(request):
    # Fetch the appointments either as a user or as a tax advisor
    future_appointments = Appointment.objects.filter(
        appointment_date__gte=timezone.now()
    ).filter(models.Q(user_request__user=request.user) | models.Q(tax_advisor=request.user))

    context = {
        'future_appointments': future_appointments
    }

    return render(request, 'base/dashboard.html', context)
