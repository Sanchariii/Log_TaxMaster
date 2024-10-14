from .forms import TaxCalculatorForm
from .models import TaxScheme, SurchargeRate
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal, InvalidOperation
from django.http import HttpResponseBadRequest
import logging


def clean_and_convert(value):
   value = value.replace('₹', '').replace('lakh', '').strip()
   if value.startswith('Upto'):
       value = value.replace('Upto', '').strip()
   elif value.startswith('More than'):
       value = value.replace('More than', '').strip()
       return Decimal(value) * 100000 + Decimal('0.01')
   return Decimal(value) * 100000 if value else Decimal('0.0')



def calculate_surcharge(taxable_income, tax):
    """Calculate surcharge based on income thresholds."""
    surcharge = Decimal('0.0')
    if taxable_income > 5000000 and taxable_income <= 10000000:
        surcharge = Decimal('0.1') * tax
    elif taxable_income > 10000000 and taxable_income <= 20000000:
        surcharge = Decimal('0.15') * tax
    elif taxable_income > 20000000 and taxable_income <= 50000000:
        surcharge = Decimal('0.25') * tax
    elif taxable_income > 50000000:
        surcharge = Decimal('0.37') * tax
    return surcharge

def calculate_tax_view(income, standard_deduction, other_deductions, age_group):
    """Calculate tax for both regimes and apply surcharge and cess."""
    income = Decimal(income)
    standard_deduction = Decimal(standard_deduction)
    other_deductions = Decimal(other_deductions)

    def old_regime_tax():
        taxable_income = income - standard_deduction - other_deductions
        tax = Decimal('0.0')
        if age_group == 1:  # Below 60 years
            if taxable_income <= 250000:
                tax = Decimal('0.0')
            elif taxable_income <= 500000:
                tax = Decimal('0.05') * (taxable_income - 250000)
            elif taxable_income <= 1000000:
                tax = Decimal('12500') + Decimal('0.2') * (taxable_income - 500000)
            else:
                tax = Decimal('112500') + Decimal('0.3') * (taxable_income - 1000000)
        elif age_group == 2:  # Between 60 and 80 years
            if taxable_income <= 300000:
                tax = Decimal('0.0')
            elif taxable_income <= 500000:
                tax = Decimal('0.05') * (taxable_income - 300000)
            elif taxable_income <= 1000000:
                tax = Decimal('10000') + Decimal('0.2') * (taxable_income - 500000)
            else:
                tax = Decimal('110000') + Decimal('0.3') * (taxable_income - 1000000)
        elif age_group == 3:  # Above 80 years
            if taxable_income <= 500000:
                tax = Decimal('0.0')
            elif taxable_income <= 1000000:
                tax = Decimal('0.2') * (taxable_income - 500000)
            else:
                tax = Decimal('100000') + Decimal('0.3') * (taxable_income - 1000000)
        surcharge = calculate_surcharge(taxable_income, tax)
        tax += surcharge
        cess = Decimal('0.04') * tax
        return tax + cess

    def new_regime_tax():
        taxable_income = income
        tax = Decimal('0.0')
        if taxable_income <= 250000:
            tax = Decimal('0.0')
        elif taxable_income <= 500000:
            tax = Decimal('0.05') * (taxable_income - 250000)
        elif taxable_income <= 750000:
            tax = Decimal('12500') + Decimal('0.1') * (taxable_income - 500000)
        elif taxable_income <= 1000000:
            tax = Decimal('37500') + Decimal('0.15') * (taxable_income - 750000)
        elif taxable_income <= 1250000:
            tax = Decimal('75000') + Decimal('0.2') * (taxable_income - 1000000)
        elif taxable_income <= 1500000:
            tax = Decimal('125000') + Decimal('0.25') * (taxable_income - 1250000)
        else:
            tax = Decimal('187500') + Decimal('0.3') * (taxable_income - 1500000)
        surcharge = calculate_surcharge(taxable_income, tax)
        tax += surcharge
        cess = Decimal('0.04') * tax
        return tax + cess

    tax_old_regime = old_regime_tax()
    tax_new_regime = new_regime_tax()
    return tax_old_regime, tax_new_regime



@login_required
def tax_calculator_view(request):
    if request.method == 'POST':
        form = TaxCalculatorForm(request.POST)
        if form.is_valid():
            age_group = int(form.cleaned_data['age_group'])
            income = form.cleaned_data['annual_income']
            standard_deduction = form.cleaned_data['standard_deduction']
            other_deductions = form.cleaned_data['other_deductions']
            selected_scheme = request.POST.get('selected_scheme', 'both')
            tax_old_regime, tax_new_regime = calculate_tax_view(income, standard_deduction, other_deductions, age_group)
            
            # Determine the best regime
            if tax_old_regime < tax_new_regime:
                best_regime = "Old Regime"
                suggestions = [
                    "Maximize your 80C deductions (up to Rs. 1.5 lakh) by investing in PPF, ELSS, NSC, or insurance.",
                    "Use 80D deduction for health insurance premiums (up to Rs. 50,000 for senior citizens).",
                    "Check eligibility for other deductions like 80E (education loan), 80EEA (home loan interest), and 80G (charitable donations)."
                ]
            elif tax_old_regime > tax_new_regime:
                best_regime = "New Regime"
                suggestions = [
                    "Since no deductions are allowed in the new regime, ensure your salary structure is tax-efficient.",
                    "Plan for the future by investing in tax-free bonds or tax-saving instruments outside the deduction realm."
                ]
            else:
                best_regime = "Both Regimes yield the same tax amount."
                suggestions = []

            # Determine age slab
            if age_group == 1:
                age_slab = "Below 60"
            elif age_group == 2:
                age_slab = "60 to 79"
            else:
                age_slab = "80 and above"

            # Happy message if no suggestions are needed
            happy_message = "Great news 🎉! You don't need to pay any tax this Year!"

            return render(request, 'calculator/results.html', {
                'form': form,
                'tax_old_regime': tax_old_regime if selected_scheme in ['both', 'old'] else None,
                'tax_new_regime': tax_new_regime if selected_scheme in ['both', 'new'] else None,
                'best_regime': best_regime,
                'suggestions': suggestions,
                'happy_message': happy_message if not suggestions else None,
                'selected_scheme': selected_scheme,
                'user_name': request.user.username,
                'age_slab': age_slab,
                'thank_you_message': "Thank you for using our tax calculator!"
            })
     
    else:
        form = TaxCalculatorForm()
    return render(request, 'calculator/tax_calculator.html', {'form': form})



def tax_slabs_view(request):
    return render(request, 'calculator/tax_slabs.html')
