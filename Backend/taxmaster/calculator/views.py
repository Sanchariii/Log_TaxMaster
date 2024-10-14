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



# def calculate_tax(income_type, total_income, net_income, deductions, regime, age_group):
#     taxable_income = Decimal(total_income) - Decimal(deductions)
#     if income_type == 'business' and net_income:
#         taxable_income = Decimal(net_income)
    
#     if age_group == 'senior':
#         exemption_limit = Decimal('300000')
#     elif age_group == 'super_senior':
#         exemption_limit = Decimal('500000')
#     else:
#         exemption_limit = Decimal('250000')
    
#     tax = Decimal('0')
#     if regime == 'old':
#         if taxable_income <= exemption_limit:
#             tax = Decimal('0')
#         elif taxable_income <= 500000:
#             tax = (taxable_income - exemption_limit) * Decimal('0.05')
#         elif taxable_income <= 1000000:
#             tax = Decimal('12500') + (taxable_income - 500000) * Decimal('0.2')
#         else:
#             tax = Decimal('12500') + Decimal('100000') + (taxable_income - 1000000) * Decimal('0.3')
#     else:
#         if taxable_income <= 250000:
#             tax = Decimal('0')
#         elif taxable_income <= 500000:
#             tax = (taxable_income - 250000) * Decimal('0.05')
#         elif taxable_income <= 750000:
#             tax = Decimal('12500') + (taxable_income - 500000) * Decimal('0.1')
#         elif taxable_income <= 1000000:
#             tax = Decimal('12500') + Decimal('25000') + (taxable_income - 750000) * Decimal('0.15')
#         elif taxable_income <= 1250000:
#             tax = Decimal('12500') + Decimal('25000') + Decimal('37500') + (taxable_income - 1000000) * Decimal('0.2')
#         elif taxable_income <= 1500000:
#             tax = Decimal('12500') + Decimal('25000') + Decimal('37500') + Decimal('50000') + (taxable_income - 1250000) * Decimal('0.25')
#         else:
#             tax = Decimal('12500') + Decimal('25000') + Decimal('37500') + Decimal('50000') + Decimal('62500') + (taxable_income - 1500000) * Decimal('0.3')
    
#     # Add health and education cess
#     tax += tax * Decimal('0.04')
    
#     # Calculate surcharge
#     surcharge = Decimal('0.0')
#     if taxable_income > 5000000:
#         surcharge = tax * Decimal('0.37')
#     elif taxable_income > 2000000:
#         surcharge = tax * Decimal('0.25')
#     elif taxable_income > 1000000:
#         surcharge = tax * Decimal('0.15')
#     elif taxable_income > 500000:
#         surcharge = tax * Decimal('0.10')
    
#     tax += surcharge
#     return tax

def calculate_tax_view(request):
    user = request.user
    try:
        user_details = UserDetails.objects.get(user=user)
    except UserDetails.DoesNotExist:
        return redirect('user_details')

    if request.method == 'POST':
        form = TaxCalculatorForm(request.POST)
        if form.is_valid():
            income_type = form.cleaned_data['income_type']
            total_income = form.cleaned_data['total_income']
            net_income = form.cleaned_data.get('net_income')  # Optional for business income
            deductions = form.cleaned_data['deductions']
            age_group = form.cleaned_data['age_group']

            # Calculate tax under Old Regime
            tax_old_regime = calculate_tax_old_regime(
                income_type=income_type,
                age_group=age_group,
                gross_income=total_income,
                deductions_80C=deductions,
                #health_insurance=deductions  # Assuming health insurance is part of deductions
            )

            # Calculate tax under New Regime
            tax_new_regime = calculate_tax_new_regime(
                income_type=income_type,
                gross_income=total_income
            )

            # Recommend the tax regime based on tax amounts
            old_tax, new_tax, recommendation = recommend_tax_regime(
                total_income, 
                deductions,  # Total deductions
                income_type, 
                net_income, 
                age_group
            )

            context = {
                'form': form,
                'user_details': user_details,
                'tax_old_regime': tax_old_regime,
                'tax_new_regime': tax_new_regime,
                'old_tax': old_tax,
                'new_tax': new_tax,
                'recommendation': recommendation
            }

            return render(request, 'calculator/tax_result.html', context)
    else:
        exemption_limit = Decimal('250000')
    
    tax = Decimal('0')
    if regime == 'old':
        if taxable_income <= exemption_limit:
            tax = Decimal('0')
        elif taxable_income <= 500000:
            tax = (taxable_income - exemption_limit) * Decimal('0.05')
        elif taxable_income <= 1000000:
            tax = Decimal('12500') + (taxable_income - 500000) * Decimal('0.2')
        else:
            tax = Decimal('12500') + Decimal('100000') + (taxable_income - 1000000) * Decimal('0.3')
    else:
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
    
    # Add health and education cess
    tax += tax * Decimal('0.04')
    
    # Calculate surcharge
    surcharge = Decimal('0.0')
    if taxable_income > 50000000:
        surcharge = tax * Decimal('0.37')
    elif taxable_income > 20000000:
        surcharge = tax * Decimal('0.25')
    elif taxable_income > 10000000:
        surcharge = tax * Decimal('0.15')
    elif taxable_income > 5000000:
        surcharge = tax * Decimal('0.10')
    
    tax += surcharge
    return tax

def recommend_tax_regime(income, deductions, income_type, net_income, age_group):
   old_tax = calculate_tax(income_type, income, net_income, deductions, 'old', age_group)
   new_tax = calculate_tax(income_type, income, net_income, deductions, 'new', age_group)
   if old_tax == 0 and new_tax == 0:
       recommendation = "Great news! You don't have to pay any taxes this year! 🎉"
   elif old_tax < new_tax:
       savings = new_tax - old_tax
       recommendation = f"Old Tax Regime is recommended for you. It would save you ₹{savings:.2f} in taxes."
   else:
       savings = old_tax - new_tax
       recommendation = f"New Tax Regime is recommended for you. It would save you ₹{savings:.2f} in taxes."
   return old_tax, new_tax, recommendation
        form = TaxCalculatorForm()

    return render(request, 'calculator/tax_calculator.html', {'form': form})

# def recommend_tax_regime(income, deductions, income_type, net_income, age_group):
#    old_tax = calculate_tax(income_type, income, net_income, deductions, 'old', age_group)
#    new_tax = calculate_tax(income_type, income, net_income, deductions, 'new', age_group)
#    if old_tax == 0 and new_tax == 0:
#        recommendation = "Great news! You don't have to pay any taxes this year! 🎉"
#    elif old_tax < new_tax:
#        savings = new_tax - old_tax
#        recommendation = f"Old Tax Regime is recommended for you. It would save you ₹{savings:.2f} in taxes."
#    else:
#        savings = old_tax - new_tax
#        recommendation = f"New Tax Regime is recommended for you. It would save you ₹{savings:.2f} in taxes."
#    return old_tax, new_tax, recommendation


def recommend_tax_regime(income, deductions, income_type, net_income, age_group):
    old_tax = calculate_tax_old_regime(
        income_type=income_type,
        age_group=age_group,
        gross_income=income,
        deductions_80C=deductions,
        health_insurance=0  # No additional deductions for new regime
    )
    new_tax = calculate_tax_new_regime(
        income_type=income_type,
        gross_income=income
    )
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
   user = request.user
#    try:
#        user_details = UserDetails.objects.get(user=user)
#    except UserDetails.DoesNotExist:
#        return redirect('user_details')
   if request.method == 'POST':
       form = TaxCalculatorForm(request.POST)
       if form.is_valid():
           income_type = form.cleaned_data['income_type']
           total_income = form.cleaned_data['total_income']
           net_income = form.cleaned_data['net_income']
        #    regime = form.cleaned_data['regime']
           deductions = form.cleaned_data['deductions']
           age_group = form.cleaned_data['age_group']
           old_tax, new_tax, recommendation = recommend_tax_regime(total_income, deductions, income_type, net_income, age_group)
           context = {
               'form': form,
               'old_tax': old_tax,
               'new_tax': new_tax,
               'recommendation': recommendation,
            #    'user_details': user_details,
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
       income_type= request.POST.get('income_type')
       net_income = request.POST.get('net_income', '0')
       age_group = request.POST.get('age_group')
       deductions = request.POST.get('deductions')
    #    if user_details_id is None:
    #        return HttpResponseBadRequest("Missing parameters.")
    #    user_details = get_object_or_404(UserDetails, id=user_details_id)
       try:
           income_decimal = Decimal(income_type.replace(',', '').strip())
           deductions_decimal = Decimal(deductions.replace(',', '').strip())
       except (ValueError, InvalidOperation) as e:
           logger.error("Error converting income or deductions: %s", e)
           return HttpResponseBadRequest("Invalid number format for income or deductions.")
       old_regime_tax = calculate_tax(income_type, income_decimal, net_income, deductions_decimal, 'old', age_group)
       new_regime_tax = calculate_tax(income_type, income_decimal, net_income, deductions_decimal, 'new', age_group)
       context = {
        #    'user_details': user_details,
           'income': income_decimal,
           'deductions': deductions_decimal,
           'old_tax': old_regime_tax,
           'new_tax': new_regime_tax,
       }
       pdf = render_to_pdf('calculator/results_pdf.html', context)
       if pdf.err:
           return HttpResponse('Error rendering PDF', status=400)
       response = HttpResponse(pdf, content_type='application/pdf')
       response['Content-Disposition'] = 'attachment; filename="tax_calculation_result.pdf"'
       return response


# def print_pdf_view(request):
#    if request.method == 'POST':
#        user_details_id = request.POST.get('user_details_id')
#        income_type= request.POST.get('income_type')
#        net_income = request.POST.get('net_income', '0')
#        age_group = request.POST.get('age_group')
#        deductions = request.POST.get('deductions')
#        if user_details_id is None:
#            return HttpResponseBadRequest("Missing parameters.")
#        user_details = get_object_or_404(UserDetails, id=user_details_id)
#        try:
#            income_decimal = Decimal(income_type.replace(',', '').strip())
#            deductions_decimal = Decimal(deductions.replace(',', '').strip())
#        except (ValueError, InvalidOperation) as e:
#            logger.error("Error converting income or deductions: %s", e)
#            return HttpResponseBadRequest("Invalid number format for income or deductions.")
#        old_regime_tax = calculate_tax(income_type, income_decimal, net_income, deductions_decimal, 'old', age_group)
#        new_regime_tax = calculate_tax(income_type, income_decimal, net_income, deductions_decimal, 'new', age_group)
#        context = {
#            'user_details': user_details,
#            'income': income_decimal,
#            'deductions': deductions_decimal,
#            'old_tax': old_regime_tax,
#            'new_tax': new_regime_tax,
#        }
#        pdf = render_to_pdf('calculator/results_pdf.html', context)
#        if pdf.err:
#            return HttpResponse('Error rendering PDF', status=400)
#        response = HttpResponse(pdf, content_type='application/pdf')
#        response['Content-Disposition'] = 'attachment; filename="tax_calculation_result.pdf"'
#        return response
#    else:
#        return HttpResponseBadRequest("Invalid request method. Please submit the form to generate the PDF.")
   






def calculate_tax_old_regime(income_type, age_group, gross_income, deductions_80C, health_insurance):
   tax = 0
   # Determine age-based slab
   if age_group == 'below_60':
       age_based_slab = 250000  # for individuals below 60 years
   elif age_group == '60_80':
       age_based_slab = 300000  # for senior citizens (60-80 years)
   else:
       age_based_slab = 500000  # for super senior citizens (above 80 years)
   if income_type == 'salaried':
       standard_deduction = 50000
       taxable_income = gross_income - standard_deduction - deductions_80C - health_insurance
       # Old Regime Slabs based on age
       if taxable_income <= age_based_slab:
           tax = 0
       elif age_based_slab < taxable_income <= 500000:
           tax = 0.05 * (taxable_income - age_based_slab)
       elif 500000 < taxable_income <= 1000000:
           tax = 12500 + 0.2 * (taxable_income - 500000)
       else:
           tax = 112500 + 0.3 * (taxable_income - 1000000)
   elif income_type == 'business':
       taxable_income = gross_income - deductions_80C - health_insurance
       # Business person uses the same slab as old regime based on age
       if taxable_income <= age_based_slab:
           tax = 0
       elif age_based_slab < taxable_income <= 500000:
           tax = 0.05 * (taxable_income - age_based_slab)
       elif 500000 < taxable_income <= 1000000:
           tax = 12500 + 0.2 * (taxable_income - 500000)
       else:
           tax = 112500 + 0.3 * (taxable_income - 1000000)
   return round(tax, 2)

def calculate_tax_new_regime(income_type, gross_income):
    tax = Decimal(0)
    # New Regime Slabs (fixed, not age dependent)
    taxable_income = Decimal(gross_income)
    if taxable_income <= Decimal(250000):
        tax = Decimal(0)
    elif Decimal(250000) < taxable_income <= Decimal(500000):
        tax = Decimal(0.05) * (taxable_income - Decimal(250000))
    elif Decimal(500000) < taxable_income <= Decimal(750000):
        tax = Decimal(12500) + Decimal(0.1) * (taxable_income - Decimal(500000))
    elif Decimal(750000) < taxable_income <= Decimal(1000000):
        tax = Decimal(37500) + Decimal(0.15) * (taxable_income - Decimal(750000))
    elif Decimal(1000000) < taxable_income <= Decimal(1250000):
        tax = Decimal(75000) + Decimal(0.2) * (taxable_income - Decimal(1000000))
    elif Decimal(1250000) < taxable_income <= Decimal(1500000):
        tax = Decimal(125000) + Decimal(0.25) * (taxable_income - Decimal(1250000))
    else:
        tax = Decimal(187500) + Decimal(0.3) * (taxable_income - Decimal(1500000))
    return round(tax, 2)



def income_view(request):
   if request.method == 'POST':
       form = TaxCalculatorForm(request.POST)
       if form.is_valid():
           income_details = form.cleaned_data
           # Calculate tax for both Old and New Regime
           tax_old_regime = calculate_tax_old_regime(
               income_type=income_details['income_type'],
               age_group=income_details['age_group'],
               gross_income=income_details['gross_income'],
               deductions_80C=income_details['deductions_80C'],
               health_insurance=income_details['health_insurance']
           )
           tax_new_regime = calculate_tax_new_regime(
               income_type=income_details['income_type'],
               gross_income=income_details['gross_income']
           )
           return render(request, 'tax_result.html', {
               'tax_old_regime': tax_old_regime,
               'tax_new_regime': tax_new_regime,
               'form': form
           })
   else:
       form = TaxCalculatorForm()
   return render(request, 'income_form.html', {'form': form})