from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserRequest, TaxAdvisorProfile
from .forms import TaxAdvisorProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

############################# Available Advisors View ######################################################
@login_required
def available_advisors_view(request):
    # Filter only advisors who belong to the 'Tax Advisor' group and have license and experience
    advisors = User.objects.filter(
        groups__name='Tax Advisor', 
        taxadvisorprofile__isnull=False,  # Ensures a related profile exists
        taxadvisorprofile__license_serial__isnull=False,
        taxadvisorprofile__years_of_experience__isnull=False
    ).exclude(
        taxadvisorprofile__license_serial='',  # Exclude advisors with an empty license serial
        taxadvisorprofile__years_of_experience=0  # Exclude advisors with zero years of experience
    ).select_related('taxadvisorprofile')

    
    return render(request, 'advisor/available_advisors.html', {'advisors': advisors})


############################# Request to Advisor ######################################################
def advisor_requests(request):
    if request.user.groups.filter(name='Tax Advisor').exists():  # Check if user belongs to the 'Tax Advisor' group
        # Show only requests where the current user is the tax advisor and either approved or rejected
        requests = UserRequest.objects.filter(tax_advisor=request.user).filter(approved=True) | UserRequest.objects.filter(tax_advisor=request.user).filter(rejected=True)
    else:
        requests = None  # Handle case where the user is not a tax advisor

    return render(request, 'advisor/advisor_requests.html', {
        'requests': requests,
    })



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserRequest, TaxAdvisorProfile
from .forms import TaxAdvisorProfileForm


############################# Tax Advisor Profile ######################################################
def tax_advisor_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Check if the TaxAdvisorProfile exists, if not, create one with default values
    profile, created = TaxAdvisorProfile.objects.get_or_create(
        user=user,
        defaults={
            'license_serial': '',
            'years_of_experience': 0,
            'gender': 'not_specified'
        }
    )

    if request.method == 'POST':
        form = TaxAdvisorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('advisor_requests')
    else:
        form = TaxAdvisorProfileForm(instance=profile)

    return render(request, 'advisor/tax_advisor_profile.html', {'form': form, 'user': user, 'profile': profile})



############################# Tax Advisor Profile View ######################################################
class TaxAdvisorProfileView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            profile = TaxAdvisorProfile.objects.get(user=request.user)
        except TaxAdvisorProfile.DoesNotExist:
            return redirect('create_profile')  # Redirect if profile doesn't exist

        return render(request, 'advisor/tax_advisor_profile_view.html', {'profile': profile, 'user': request.user})


############################# Editing Tax Advisor Profile ######################################################
class TaxAdvisorProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            profile = TaxAdvisorProfile.objects.get(user=request.user)
        except TaxAdvisorProfile.DoesNotExist:
            return redirect('create_profile')  # Redirect if profile doesn't exist

        form = TaxAdvisorProfileForm(instance=profile)
        return render(request, 'advisor/edit_tax_advisor_profile.html', {'form': form, 'user': request.user})

    def post(self, request):
        profile = TaxAdvisorProfile.objects.get(user=request.user)
        form = TaxAdvisorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile view after save
        return render(request, 'advisor/edit_tax_advisor_profile.html', {'form': form, 'user': request.user})

