from django.shortcuts import render
from .forms import UserDetailsForm, SurchargeForm
from .models import UserDetails, TaxScheme, SurchargeRate

def clean_and_convert(value):
    """Cleans and converts a given string value to float."""
    # Remove unwanted characters and extra spaces
    value = value.replace('₹', '').replace('lakh', '').strip()
    
    # Handle specific phrases
    if value.startswith('Upto'):
        value = value.replace('Upto', '').strip()
    elif value.startswith('More than'):
        value = value.replace('More than', '').strip()
        # Assuming "More than X" means X + 1 for tax calculation purposes
        value = str(float(value) + 0.00001)

    # Convert the cleaned value to float, default to 0.0 if empty
    return float(value) if value else 0.0

def calculate_tax(income, deductions, regime):
    taxable_income = income - deductions if regime == 'old' else income
    tax = 0
    tax_slabs = TaxScheme.objects.filter(regime=regime).order_by('rate')
    
    for slab in tax_slabs:
        slab_range = slab.slab.split(' - ')
        
        # Clean and convert lower limit
        lower_limit = clean_and_convert(slab_range[0])
        
        # Clean and convert upper limit if it exists
        if len(slab_range) > 1:
            upper_limit = clean_and_convert(slab_range[1])
        else:
            upper_limit = float('inf')  # Handle case where there's no upper limit

        if taxable_income > lower_limit: 
            tax += (min(taxable_income, upper_limit) - lower_limit) * (slab.rate / 100)
    
    return tax

def user_details_view(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            user_details = form.save()
            user_details.user = request.user

            # Check if deductions is a list or a single value
            if isinstance(user_details.deductions, list):
                total_deductions = sum(user_details.deductions)
            else:
                total_deductions = user_details.deductions  # Use it directly if it's not a list

            old_regime_tax = calculate_tax(user_details.income, total_deductions, 'old')
            new_regime_tax = calculate_tax(user_details.income, total_deductions, 'new')

            return render(request, 'calculator/results.html', {
                'user_details': user_details,
                'old_regime_tax': old_regime_tax,
                'new_regime_tax': new_regime_tax,
            })
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