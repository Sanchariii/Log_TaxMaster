from django.shortcuts import render
from django.contrib.auth.models import Group, User

def available_advisors_view(request):
    advisors = User.objects.filter(groups__name='Tax Advisor')
    return render(request, 'appointments/available_advisors.html', {'advisors': advisors})
