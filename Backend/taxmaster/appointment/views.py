from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm, AvailabilityCheckForm
from calculator.models import UserRequest

# View for checking advisor availability
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User



@login_required
def available_dates_view(request):
    # Check if the user is in the 'Tax Advisor' group
    is_tax_advisor = request.user.groups.filter(name='Tax Advisor').exists()
    
    # If the user is not a tax advisor, return an error or a different context
    if not is_tax_advisor:
        return render(request, 'appointment/not_authorized.html')

    # Generate available dates (for example, next 30 days)
    today = timezone.now().date()
    available_dates = [today + timedelta(days=i) for i in range(30)]

    return render(request, 'appointment/available_dates.html', {
        'available_dates': available_dates,
    })

def check_availability(request):
    available_slots = None
    if request.method == "POST":
        form = AvailabilityCheckForm(request.POST)
        if form.is_valid():
            advisor = form.cleaned_data['advisor']
            date = form.cleaned_data['date']
            # Query for appointments for the advisor on the given date
            available_slots = Appointment.objects.filter(tax_advisor=advisor, appointment_date__date=date)
    else:
        form = AvailabilityCheckForm()

    return render(request, 'appointment/check_availability.html', {
        'form': form,
        'available_slots': available_slots,
    })

# View for booking an appointment
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user_request = request.user.requests.first()  # Assuming a single user request
            appointment.save()
            return render(request, 'appointment/appointment_success.html', {'appointment': appointment})
    else:
        form = AppointmentForm()

    return render(request, 'appointment/book_appointment.html', {'form': form})

@login_required
def create_appointment_view(request, user_request_id):
    user_request = UserRequest.objects.get(id=user_request_id)
    
    if request.method == 'POST':
        tax_advisor_id = request.POST.get('tax_advisor')  # Assume this comes from a form
        appointment_date = request.POST.get('appointment_date')
        notes = request.POST.get('notes')
        
        # Check if the selected user is in the "Tax Advisor" group
        tax_advisor = User.objects.get(id=tax_advisor_id)
        if tax_advisor.groups.filter(name='Tax Advisor').exists():
            appointment = Appointment.objects.create(
                user_request=user_request,
                tax_advisor=tax_advisor,
                appointment_date=appointment_date,
                notes=notes
            )
            return redirect('appointment_success')  # Redirect to a success page
    
    # Get all users in the "Tax Advisor" group for the form
    tax_advisors = User.objects.filter(groups__name='Tax Advisor')
    
    return render(request, 'calculator/create_appointment.html', {
        'user_request': user_request,
        'tax_advisors': tax_advisors,
    })