from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from appointment.models import Appointment
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import is_User_or_Advisor
from advisor.models import UserRequest
from django.db import models
# from .forms import UserDetailsForm
# from .models import UserDetails
from decimal import Decimal
from calculator.views import calculate_tax_view


############################# Home Page ####################################################### 

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




def user_appointments_view(request):
    user = request.user
    # Filter based on the `confirmed` field, which indicates approval status
    approved_appointments = UserRequest.objects.filter(user=user, approved=True)
    requested_appointments = UserRequest.objects.filter(user=user, approved=False)

    context = {
        'approved_appointments': approved_appointments,
        'requested_appointments': requested_appointments,
    }

    return render(request, 'base/user_appointments.html', context)


from django.shortcuts import render
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def home_view(request):
    # favicon_path = "C:/Users/SRay5/OneDrive - Rockwell Automation, Inc/Desktop/TaxMaster/Frontend/tax_favicon.jpg"
    # favicon_base64 = get_base64_image(favicon_path)

    # # Pass favicon_base64 to the template context
    # context = {
    #     'favicon_base64': favicon_base64,
    # }

    return render(request, 'base/home.html')



def learn_more(request):
    return render(request, 'base/learn_more.html')

