from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm, AvailabilityCheckForm, AppointmentRequestForm
from advisor.models import UserRequest
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.models import User



# @login_required
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
    available_slots = []
    if request.method == "POST":
        form = AvailabilityCheckForm(request.POST)
        if form.is_valid():
            advisor = form.cleaned_data['advisor']
            date = form.cleaned_data['date']
            # Fetch all appointments for the advisor on the selected date
            booked_slots = Appointment.objects.filter(
                tax_advisor=advisor,
                appointment_date__date=date
            ).values_list('appointment_time', flat=True)  # Adjust field name if needed

            # Define your working hours for the advisor
            start_time = timezone.datetime.combine(date, timezone.datetime.min.time())
            end_time = timezone.datetime.combine(date, timezone.datetime.max.time())
            time_slots = [
                start_time + timedelta(hours=i) for i in range(9, 17)  # Example: 9 AM to 5 PM
            ]

            # Filter available time slots by removing booked slots
            available_slots = [slot for slot in time_slots if slot not in booked_slots]

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

# @login_required
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
    
from datetime import timedelta
from django.utils import timezone

def get_available_dates(advisor):
    today = timezone.now().date()  # Current date
    available_dates = []
    
    # Check the availability for the next 30 days from today
    for i in range(1, 31):  # Start from tomorrow (i=1), check for the next 30 days
        date_to_check = today + timedelta(days=i)
        
        # Find appointments for the tax advisor on the date_to_check
        appointments = Appointment.objects.filter(
            tax_advisor=advisor,
            appointment_date=date_to_check
        )
        
        # If no appointments exist for the date, add it to available dates
        if not appointments.exists():
            available_dates.append(date_to_check)
    
    return available_dates


    
def request_appointment(request, advisor_id):
    advisor = get_object_or_404(User, id=advisor_id)

    # Get available future dates for the advisor (e.g., next 30 days)
    available_dates = get_available_dates(advisor)
    future_dates = [date for date in available_dates if date > timezone.now().date()]

    form = AppointmentRequestForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            print("Form is valid")

            # Create appointment but don't commit yet
            appointment = form.save(commit=False)
            appointment.tax_advisor = advisor
            appointment.user = request.user  # Associate the appointment with the logged-in user
            appointment.appointment_date = form.cleaned_data['requested_date']  # Assign the requested date
            appointment.slot = form.cleaned_data['slot']  # Assign the requested slot (make sure form has this field)

            # Create a new UserRequest entry
            user_request = UserRequest.objects.create(
                user=request.user,
                tax_advisor=advisor,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
                slot=appointment.slot,  # Add slot to UserRequest model
                date=appointment.appointment_date  # Add date to UserRequest model
            )

            # Associate the appointment with the user request
            appointment.user_request = user_request
            appointment.save()

            print("Appointment saved, redirecting...")
            return redirect('appointment_request_sent')  # Ensure this URL name is defined
        else:
            print("Form errors:", form.errors)  # Print validation errors

    return render(request, 'appointment/request_appointment.html', {
        'form': form,
        'advisor': advisor,
        'available_dates': future_dates,
    })
    
def appointment_request_already_submitted(request):
    return render(request, 'appointment/appointment_request_already_submitted.html')


def appointment_request_sent(request):
    return render(request, 'appointment/appointment_request_sent.html')
    
def manage_requests_view(request):
    if request.user.groups.filter(name='Tax Advisor').exists():
        requests = UserRequest.objects.filter(tax_advisor=request.user, approved=False, rejected=False)
        return render(request, 'appointment/manage_requests.html', {'requests': requests})
    else:
        return redirect('not_authorized')

def approved_requests(request):
    requests = UserRequest.objects.filter(user=request.user, approved=True)
    return render(request, 'appointment/approved_requests.html', {'requests': requests})

def approve_request(request, request_id):
    user_request = UserRequest.objects.get(id=request_id, tax_advisor=request.user)
    user_request.approved = True
    user_request.save()

    send_mail(
            'Your Appointment Request Has Been Approved',
            f'Hello {user_request.first_name},\n\nYour appointment request with {user_request.tax_advisor.first_name} {user_request.tax_advisor.last_name} has been approved. Please check your account for more details.',
            settings.DEFAULT_FROM_EMAIL,
            [user_request.email],
            fail_silently=False,
        )

    return redirect('manage_requests')

    

def reject_request(request, request_id):
    user_request = get_object_or_404(UserRequest, id=request_id, tax_advisor=request.user)
    user_request.rejected = True
    user_request.save()

    send_mail(
        'Your Appointment Request Has Been Rejected',
        f'Hello {user_request.first_name},\n\nYour appointment request with {user_request.tax_advisor.first_name} {user_request.tax_advisor.last_name} has been rejected. Please check your account for more details.',
        settings.DEFAULT_FROM_EMAIL,
        [user_request.email],
        fail_silently=False,
    )

    return redirect('manage_requests')


def advisor_appointments_view(request):
    if request.user.groups.filter(name='Tax Advisor').exists():
        approved_users = UserRequest.objects.filter(tax_advisor=request.user, approved=True)
        return render(request, 'appointments/advisor_appointments.html', {'approved_users': approved_users})
    else:
        return redirect('not_authorized')


def user_appointments(request):
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(user=request.user)
    else:
        appointments = None

    return render(request, 'appointment/user_appointments.html', {
        'appointments': appointments
    })