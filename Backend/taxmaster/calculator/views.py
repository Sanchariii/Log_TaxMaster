from django.shortcuts import render
from .forms import UserDetailsForm, SurchargeForm
from .models import UserDetails, TaxScheme, SurchargeRate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def calculate_tax(income, deductions, regime):
    taxable_income = income - deductions if regime == 'old' else income
    tax = 0
    tax_slabs = TaxScheme.objects.filter(regime=regime).order_by('rate')
    for slab in tax_slabs:
        slab_range = slab.slab.split(' - ')
        lower_limit = float(slab_range.replace('₹', '').replace('lakh', '').strip()) * 100000
        upper_limit = float(slab_range.replace('₹', '').replace('lakh', '').strip()) * 100000 if len(slab_range) > 1 else float('inf')
        if taxable_income > lower_limit:
            tax += (min(taxable_income, upper_limit) - lower_limit) * (slab.rate / 100)
    return tax



@login_required
def user_details_view(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            user_details = form.save(commit=False)
            if request.user.is_authenticated:
                user_details.user = request.user
                user_details.save()
                old_regime_tax = calculate_tax(user_details.income, user_details.deductions, 'old')
                new_regime_tax = calculate_tax(user_details.income, user_details.deductions, 'new')
                return render(request, 'calculator/results.html', {
                    'user_details': user_details,
                    'old_regime_tax': old_regime_tax,
                    'new_regime_tax': new_regime_tax,
                })
            else:
                return HttpResponseForbidden("You must be logged in to submit details.")
    else:
        form = UserDetailsForm()
    return render(request, 'calculator/user_details.html', {'form': form})

def old_tax_scheme_view(request):
    old_tax_scheme = TaxScheme.objects.filter(regime='old')
    return render(request, 'calculator/old_tax_scheme.html', {'tax_scheme': old_tax_scheme})

def new_tax_scheme_view(request):
    new_tax_scheme = TaxScheme.objects.filter(regime='new')
    return render(request, 'calculator/new_tax_scheme.html', {'tax_scheme': new_tax_scheme})


def surcharge_tax_view(request):
    surcharge_rates = SurchargeRate.objects.all()

    if request.method == 'POST':
        form = SurchargeForm(request.POST)
        if form.is_valid():
            income = form.cleaned_data['income']
            surcharge = 0

            for rate in surcharge_rates:
                slab_range = rate.slab.split(' - ')
                lower_limit = float(slab_range.replace('₹', '').replace('lakh', '').strip()) * 100000
                upper_limit = float(slab_range.replace('₹', '').replace('lakh', '').strip()) * 100000 if len(slab_range) > 1 else float('inf')
                if income > lower_limit:
                    surcharge += (min(income, upper_limit) - lower_limit) * (rate.rate / 100)

            return render(request, 'calculator/surcharge_results.html', {
                'income': income,
                'surcharge': surcharge,
                'surcharge_rates': surcharge_rates,
            })
    else:
        form = SurchargeForm()

    return render(request, 'calculator/surcharge_tax.html', {'form': form, 'surcharge_rates': surcharge_rates})