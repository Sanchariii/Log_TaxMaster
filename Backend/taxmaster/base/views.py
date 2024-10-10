from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from appointment.models import Appointment
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import is_User_or_Advisor
from advisor.models import UserRequest
from django.db import models
from .forms import UserDetailsForm
from .models import UserDetails
from decimal import Decimal
from calculator.views import calculate_tax

def home_view(request):
    return render(request, 'base/home.html')

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


@login_required
def user_details_view(request):
    user = request.user
    try:
        # Check if UserDetails already exists for the current user
        user_details = UserDetails.objects.get(user=user)
    except UserDetails.DoesNotExist:
        user_details = None  # No user details exist, we will create them if needed

    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=user_details)  # Pass existing instance if available
        if form.is_valid():
            # If the form is valid, save or update the UserDetails instance
            user_details = form.save(commit=False)
            user_details.user = user  # Associate the current user
            user_details.save()  # Save the instance (create if new, update if exists)
            return redirect('tax_calculator')

    else:
        # Show the form, pre-filling if UserDetails already exists
        form = UserDetailsForm(instance=user_details)

    return render(request, 'base/user_details.html', {'form': form})
