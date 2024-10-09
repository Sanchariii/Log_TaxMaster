from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Task, Appointment
# from streamlit_django_integration import st_django_component

def hello_world(request):
    return HttpResponse("Hello, World!")

@login_required
@user_passes_test(is_User_or_Advisor)
def dashboard(request):
    future_tasks = Task.objects.filter(due_date__gte=timezone.now(), assigned_to=request.user)
    future_appointments = Appointment.objects.filter(start_time__gte=timezone.now(), attendees=request.user)

    context = {
        'future_tasks': future_tasks,
        'future_appointments': future_appointments
    }

    return render(request, 'dashboard.html', context)