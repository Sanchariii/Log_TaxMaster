from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from .models import UserRequest
import accounts.views as av

def available_advisors_view(request):
    advisors = User.objects.filter(groups__name='Tax Advisor')
    return render(request, 'advisor/available_advisors.html', {'advisors': advisors})

def advisor_requests(request):
    if av.is_taxadvisor:  # Assuming you have a way to check if the user is an advisor
        requests = UserRequest.objects.filter(tax_advisor=request.user)
    else:
        requests = None  # or handle accordingly

    return render(request, 'advisor/advisor_requests.html', {
        'requests': requests,
    })