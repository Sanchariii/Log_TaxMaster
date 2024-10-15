from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from .models import UserRequest, TaxAdvisorProfile
import accounts.views as av
from .forms import TaxAdvisorProfileForm


def available_advisors_view(request):
    # Filter only advisors who belong to the 'Tax Advisor' group and have license and experience
    advisors = User.objects.filter(
        groups__name='Tax Advisor', 
        tax_advisor_profile__isnull=False,  # Ensures a related profile exists
        tax_advisor_profile__license_serial__isnull=False,
        tax_advisor_profile__years_of_experience__isnull=False
    ).exclude(
        tax_advisor_profile__license_serial='',  # Exclude advisors with an empty license serial
        tax_advisor_profile__years_of_experience=0  # Exclude advisors with zero years of experience
    )

    
    return render(request, 'advisor/available_advisors.html', {'advisors': advisors})



def advisor_requests(request):
    if request.user.groups.filter(name='Tax Advisor').exists():  # Check if user belongs to the 'Tax Advisor' group
        # Show only requests where the current user is the tax advisor and either approved or rejected
        requests = UserRequest.objects.filter(tax_advisor=request.user).filter(approved=True) | UserRequest.objects.filter(tax_advisor=request.user).filter(rejected=True)
    else:
        requests = None  # Handle case where the user is not a tax advisor

    return render(request, 'advisor/advisor_requests.html', {
        'requests': requests,
    })

    


def tax_advisor_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Fetch the user based on user_id

    if request.method == 'POST':
        form = TaxAdvisorProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user  # Associate with the fetched user
            profile.save()
            return redirect('advisor_requests')  # Redirect to success page
    else:
        form = TaxAdvisorProfileForm()

    return render(request, 'advisor/tax_advisor_profile.html', {'form': form, 'user': user})