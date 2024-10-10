from .forms import TaxCalculatorForm
from .models import UserDetails, TaxScheme, SurchargeRate
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
    """Cleans and converts a given string value to a Decimal representing actual numbers (₹ in lakhs)."""
    # Remove currency symbol and unit, then trim extra spaces
    value = value.replace('₹', '').replace('lakh', '').strip()
    
    # Handle ranges like "Upto" or "More than"
    if value.startswith('Upto'):
        value = value.replace('Upto', '').strip()  # Take the upper bound of "Upto X lakh"
    elif value.startswith('More than'):
        value = value.replace('More than', '').strip()
        return Decimal(value) * 100000 + Decimal('0.01')  # Slightly more than X lakh

    # Convert the cleaned value to Decimal and scale by 100,000 (for lakhs)
    return Decimal(value) * 100000 if value else Decimal('0.0')

def calculate_tax(income, deductions, regime):
    taxable_income = Decimal(income) - Decimal(deductions)

    # Initialize tax variable
    tax = Decimal('0')

    # Calculate tax based on the regime
    if regime == 'old':
        # Old tax regime slabs
        if taxable_income <= 250000:
            tax = Decimal('0')
        elif taxable_income <= 500000:
            tax = (taxable_income - 250000) * Decimal('0.05')
        elif taxable_income <= 1000000:
            tax = Decimal('12500') + (taxable_income - 500000) * Decimal('0.2')
        else:
            tax = Decimal('12500') + Decimal('100000') + (taxable_income - 1000000) * Decimal('0.3')
    else:
        # New tax regime slabs
        if taxable_income <= 250000:
            tax = Decimal('0')
        elif taxable_income <= 500000:
            tax = (taxable_income - 250000) * Decimal('0.05')
        elif taxable_income <= 750000:
            tax = Decimal('12500') + (taxable_income - 500000) * Decimal('0.1')
        elif taxable_income <= 1000000:
            tax = Decimal('12500') + Decimal('25000') + (taxable_income - 750000) * Decimal('0.15')
        elif taxable_income <= 1250000:
            tax = Decimal('12500') + Decimal('25000') + Decimal('37500') + (taxable_income - 1000000) * Decimal('0.2')
        elif taxable_income <= 1500000:
            tax = Decimal('12500') + Decimal('25000') + Decimal('37500') + Decimal('50000') + (taxable_income - 1250000) * Decimal('0.25')
        else:
            tax = Decimal('12500') + Decimal('25000') + Decimal('37500') + Decimal('50000') + Decimal('62500') + (taxable_income - 1500000) * Decimal('0.3')

    # Add cess (4%)
    tax += tax * Decimal('0.04')

    # Calculate surcharge based on income slabs
    surcharge = Decimal('0.0')
    
    if taxable_income > 5000000:
        surcharge += (taxable_income - 5000000) * Decimal('0.37')  # More than ₹5 crore
    elif taxable_income > 2000000:
        surcharge += (taxable_income - 2000000) * Decimal('0.25')  # ₹2 crore - ₹5 crore
        surcharge += (2000000 - 1000000) * Decimal('0.15')  # ₹1 crore - ₹2 crore
    elif taxable_income > 1000000:
        surcharge += (taxable_income - 1000000) * Decimal('0.15')  # ₹1 crore - ₹2 crore
    elif taxable_income > 500000:
        surcharge += (taxable_income - 500000) * Decimal('0.10')  # ₹50 lakh - ₹1 crore

    # Add surcharge to the total tax
    tax += surcharge

    return tax


def get_tax_suggestions(regime):
    if regime == 'old':
        return [
            "Maximize Deductions under Section 80C: Invest in PPF, EPF, NSC, and ELSS to claim deductions up to ₹1.5 lakh.",
            "Health Insurance Premiums: Claim deductions under Section 80D for health insurance premiums.",
            "Home Loan Interest: Claim deductions on home loan interest under Section 24(b) up to ₹2 lakh.",
            "Education Loan Interest: Deduction under Section 80E for interest paid on education loans.",
            "Donations: Claim deductions for donations to specified funds and charitable institutions under Section 80G."
        ]
    else:
        return [
            "Employer Contributions: Ensure your employer contributes to the National Pension System (NPS) under Section 80CCD(2).",
            "Standard Deduction: Utilize the standard deduction of ₹50,000 (increased to ₹75,000 from FY 2024-25).",
            "Transport Allowance: Specially abled taxpayers can claim transport allowances up to a specified limit.",
            "Conveyance Allowance: Exemption up to ₹1,600 per month or ₹19,200 per year for conveyance expenses."
        ]

def recommend_tax_regime(income, deductions):
    old_tax = calculate_tax(income, deductions, 'old')
    new_tax = calculate_tax(income, deductions, 'new')

    if old_tax == 0 and new_tax == 0:
        recommendation = "Great news! You don't have to pay any taxes this year! 🎉"
    elif old_tax < new_tax:
        savings = new_tax - old_tax
        recommendation = f"Old Tax Regime is recommended for you. It would save you ₹{savings:.2f} in taxes."
    else:
        savings = old_tax - new_tax
        recommendation = f"New Tax Regime is recommended for you. It would save you ₹{savings:.2f} in taxes."

    return old_tax, new_tax, recommendation

@login_required
def tax_calculator_view(request):
    # Check if the user has UserDetails
    user = request.user
    try:
        user_details = UserDetails.objects.get(user=user)
    except UserDetails.DoesNotExist:
        # If UserDetails doesn't exist, redirect to the form to collect user details
        return redirect('user_details')

    # Continue with the tax calculation logic if user details exist
    if request.method == 'POST':
        form = TaxCalculatorForm(request.POST)
        if form.is_valid():
            income = form.cleaned_data['income']
            deductions = form.cleaned_data['deductions']
            

            # Calculate taxes using the updated logic for both regimes
            old_tax = calculate_tax(income, deductions, regime='old')
            new_tax = calculate_tax(income, deductions, regime='new')
            recommendation = recommend_tax_regime(income, deductions)
            old_suggestions = get_tax_suggestions('old')
            new_suggestions = get_tax_suggestions('new')

            context = {
                'form': form,
                'old_tax': old_tax,
                'new_tax': new_tax,
                'old_suggestions': old_suggestions,
                'new_suggestions': new_suggestions,
                'recommendation': recommendation,
                'user_details': user_details,
            }

            return render(request, 'calculator/results.html', context)
    else:
        form = TaxCalculatorForm()

    return render(request, 'calculator/tax_calculator.html', {'form': form})


@login_required
def old_tax_scheme_view(request):
    old_tax_scheme = TaxScheme.objects.filter(regime='old')
    return render(request, 'calculator/old_tax_scheme.html', {'tax_scheme': old_tax_scheme})

@login_required
def new_tax_scheme_view(request):
    new_tax_scheme = TaxScheme.objects.filter(regime='new')
    return render(request, 'calculator/new_tax_scheme.html', {'tax_scheme': new_tax_scheme})

@login_required
def surcharge_tax_view(request):
    surcharge_rates = SurchargeRate.objects.all()
    return render(request, 'calculator/surcharge_tax.html', {'surcharge_rates': surcharge_rates})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    pdf = pisa.CreatePDF(html)
    return pdf


logger = logging.getLogger('calculator')  

def print_pdf_view(request):
    if request.method == 'POST':
        user_details_id = request.POST.get('user_details_id')
        income = request.POST.get('income')
        deductions = request.POST.get('deductions')

        # Validate input data
        if user_details_id is None or income is None or deductions is None:
            return HttpResponseBadRequest("Missing parameters.")

        user_details = get_object_or_404(UserDetails, id=user_details_id)

        try:
            # Sanitize input
            income_clean = income.replace(',', '').strip()
            deductions_clean = deductions.replace(',', '').strip()
            print("Type of income before conversion:", type(income_clean))
            # Convert income and deductions to Decimal
            income_decimal = Decimal(income_clean)
            deductions_decimal = Decimal(deductions_clean)
            print("Type after conversion:", type(income_decimal))
        except (ValueError, InvalidOperation) as e:
            logger.error("Error converting income or deductions: %s", e)
            return HttpResponseBadRequest("Invalid number format for income or deductions.")

        # Calculate tax for both regimes
        old_regime_tax = calculate_tax(income_decimal, deductions_decimal, 'old')
        new_regime_tax = calculate_tax(income_decimal, deductions_decimal, 'new')

        # Prepare context for PDF
        context = {
            'user_details': user_details,
            'income': income_decimal,
            'deductions': deductions_decimal,
            'old_tax': old_regime_tax,
            'new_tax': new_regime_tax,
        }

        # Render the PDF
        pdf = render_to_pdf('calculator/results_pdf.html', context)

        # Check for errors during PDF creation
        if pdf.err:
            return HttpResponse('Error rendering PDF', status=400)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="tax_calculation_result.pdf"'
        return response
    else:
        return HttpResponseBadRequest("Invalid request method. Please submit the form to generate the PDF.")
    
    
    






