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
from logs.logging_config import logger

############################################### Logs ##########################################################

# Log messages with the fixed JSON structure
def log_it(message):
    logger.info('', extra={
        'username': 'sanchari',
        'log_id': 1,
        
        'values': {
            'iserrorlog':0,
            'message': message
        }
    })
def log_fail(whatfailed,reason):
    logger.info('', extra={
        'username': 'sanchari',
        'log_id': 1,
        
        'values': {
            'iserrorlog':1,
            'whatfailed': whatfailed,
            'reason': reason
        }
    })
def log_registration(type):
    logger.info('', extra={
        'username': 'sanchari',
        'log_id': 1,
        
        
        'values': {
            'iserrorlog':0,
            'message': 'Registration Successful',
            'type': type
        }
    })
def log_calculated(age,income,deduction,regime,saving):
    logger.info('', extra={
        'username': 'sanchari',
        'log_id': 1,
        
        
        'values': {
            'iserrorlog':0,
            'message': 'Calculation Successful',
            'age': age,
            'income': income,
            'deduction': deduction,
            'regime': regime,
            'saving': saving
        }
    })
def log_appointment(id,slot):
    logger.info('', extra={
        'username': 'sanchari',
        'log_id': 1,
        
        
        'values': {
            'iserrorlog':0,
            'message': 'Appointment Booked',
            'id': id,
            'slot': slot
        }
    })

################################################### Surcharge Calculation #################################################################
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

######################################################### Calculation of old and new regime taxes #######################################################################
def calculate_tax_view(income, deduction_80c, deduction_80d, deduction_80e, deduction_80eea, deduction_80g, age_group):
    """Calculate tax for both regimes and apply surcharge and cess, including rebates."""
    income = Decimal(income)
    deduction_80c = Decimal(deduction_80c or 0)
    deduction_80d = Decimal(deduction_80d or 0)
    deduction_80e = Decimal(deduction_80e or 0)
    deduction_80eea = Decimal(deduction_80eea or 0)
    deduction_80g = Decimal(deduction_80g or 0)
    # Fixed standard deduction amounts for old and new regime
    standard_deduction_old = Decimal('50000')
    standard_deduction_new = Decimal('75000')
    
    def old_regime_tax(income, deduction_80c, deduction_80d, deduction_80e, deduction_80eea, deduction_80g, age_group):
        taxable_income = income - standard_deduction_old - deduction_80c - deduction_80d - deduction_80e - deduction_80eea - deduction_80g
        tax = Decimal('0.0')
        
        # Age-based slab calculation
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
        
        # Apply rebate for old regime if applicable
        if taxable_income <= 500000:
            tax = max(Decimal('0.0'), tax - Decimal('12500'))
        
        # Surcharge and cess
        surcharge = calculate_surcharge(taxable_income, tax)
        tax += surcharge
        
        # Apply cess only if tax is greater than zero
        if tax > 0:
            cess = Decimal('0.04') * tax
            tax += cess
        return tax
    
    def new_regime_tax(income, standard_deduction_new):
        taxable_income = income - standard_deduction_new  # Only standard deduction applies in the new regime
        tax = Decimal('0.0')
        
        # Tax slab calculation for new regime
        if taxable_income <= 300000:
            tax = Decimal('0.0')
        elif taxable_income <= 700000:
            tax = Decimal('0.05') * (taxable_income - 300000)
        elif taxable_income <= 1000000:
            tax = Decimal('15000') + Decimal('0.1') * (taxable_income - 600000)
        elif taxable_income <= 1200000:
            tax = Decimal('45000') + Decimal('0.15') * (taxable_income - 900000)
        elif taxable_income <= 1500000:
            tax = Decimal('90000') + Decimal('0.2') * (taxable_income - 1200000)
        else:
            tax = Decimal('150000') + Decimal('0.3') * (taxable_income - 1500000)
        
        # Apply rebate for new regime if applicable
        if taxable_income <= 700000:
            tax = max(Decimal('0.0'), tax - Decimal('25000'))
        
        # Surcharge and cess
        surcharge = calculate_surcharge(taxable_income, tax)
        tax += surcharge
        
        # Apply cess only if tax is greater than zero
        if tax > 0:
            cess = Decimal('0.04') * tax
            tax += cess
        return tax

    # Calculating tax under both regimes
    tax_old_regime = old_regime_tax(income, deduction_80c, deduction_80d, deduction_80e, deduction_80eea, deduction_80g, age_group)
    tax_new_regime = new_regime_tax(income, standard_deduction_new)
    return tax_old_regime, tax_new_regime


############################# Suggestions generation ####################################################### 

def generate_suggestions(income, deductions):
    suggestions = []
    
    if income < 500000:
        suggestions.append("Consider investing in PPF or ELSS to maximize your 80C deductions.")
        suggestions.append("Utilize 80D deductions for health insurance premiums to save more.")
    elif income < 1000000:
        suggestions.append("Maximize your 80C deductions by investing in NSC or life insurance.")
        suggestions.append("Look into 80E deductions if you have an education loan.")
        suggestions.append("Don't forget about 80G deductions for charitable donations.")
    else:
        suggestions.append("Invest in tax-saving bonds and instruments outside the deduction realm.")
        suggestions.append("Ensure your salary structure is tax-efficient with components like HRA and LTA.")
        suggestions.append("Consider 80EEA deductions if you have a home loan.")

    if deductions['80c'] < 150000:
        suggestions.append("You can still invest more in 80C options to save up to Rs. 1.5 lakh.")
    if deductions['80d'] < 50000:
        suggestions.append("Increase your health insurance coverage to maximize 80D deductions.")
    if deductions['80e'] == 0:
        suggestions.append("Check if you are eligible for 80E deductions for education loans.")
    if deductions['80eea'] == 0:
        suggestions.append("Look into 80EEA deductions if you have a home loan.")
    if deductions['80g'] == 0:
        suggestions.append("Consider making charitable donations to avail 80G deductions.")

    return suggestions



############################# The Result Page ####################################################### 

@login_required
def tax_calculator_view(request):
    if request.method == 'POST':
        form = TaxCalculatorForm(request.POST)
        if form.is_valid():
            age_group = int(form.cleaned_data['age_group'])
            income = form.cleaned_data['annual_income']
            deductions = {
                '80c': form.cleaned_data.get('deduction_80c', 0) or 0,
                '80d': form.cleaned_data.get('deduction_80d', 0) or 0,
                '80e': form.cleaned_data.get('deduction_80e', 0) or 0,
                '80eea': form.cleaned_data.get('deduction_80eea', 0) or 0,
                '80g': form.cleaned_data.get('deduction_80g', 0) or 0
            }
            selected_scheme = request.POST.get('selected_scheme', 'both')
            tax_old_regime, tax_new_regime = calculate_tax_view(income, deductions['80c'], deductions['80d'], deductions['80e'], deductions['80eea'], deductions['80g'], age_group)
            standard_deduction_old = 50000
            standard_deduction_new = 75000

            # Determine the best regime
            if tax_old_regime < tax_new_regime:
                best_regime = "Old Regime"
                suggestions = generate_suggestions(income, deductions)
            elif tax_old_regime > tax_new_regime:
                best_regime = "New Regime"
                suggestions = [
                    "Since the new regime doesn't allow deductions, focus on making your salary structure tax-efficient. Consider components like HRA, LTA, and food coupons.",
                    "Invest in tax-free bonds or other tax-saving instruments that aren't dependent on deductions. This can help you plan for the future while saving on taxes."
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

            log_calculated(age_slab, int(income), int(sum(deductions.values())), best_regime, float(abs(tax_old_regime - tax_new_regime)))

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
                'standard_deduction_old': standard_deduction_old,
                'standard_deduction_new': standard_deduction_new,
                'thank_you_message': "Thank you for using TaxMaster!"
            })
    else:
        form = TaxCalculatorForm()
    return render(request, 'calculator/tax_calculator.html', {'form': form})


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from decimal import Decimal


############################# PDF view ####################################################### 

@login_required
def tax_calculator_pdf_view(request):
    if request.method == 'POST':
        # Extract form data from POST request
        def safe_decimal(value):
            try:
                return Decimal(value)
            except InvalidOperation:
                return Decimal(0)
        
        
        age_group = int(request.POST.get('age_group'))
        income = Decimal(request.POST.get('annual_income'))
        deduction_80c = safe_decimal(request.POST.get('deduction_80c', 0))
        deduction_80d = safe_decimal(request.POST.get('deduction_80d', 0))
        deduction_80e = safe_decimal(request.POST.get('deduction_80e', 0))
        deduction_80eea = safe_decimal(request.POST.get('deduction_80eea', 0))
        deduction_80g = safe_decimal(request.POST.get('deduction_80g', 0))
        selected_scheme = request.POST.get('selected_scheme', 'both')

        standard_deduction_old = Decimal('50000')
        standard_deduction_new = Decimal('75000')

        # Calculate taxes using the same logic
        tax_old_regime, tax_new_regime = calculate_tax_view(
            income,  deduction_80c, deduction_80d, deduction_80e, deduction_80eea, deduction_80g, age_group
        )

        # Determine the best regime
        if tax_old_regime < tax_new_regime:
            best_regime = "Old Regime"
            suggestions = generate_suggestions(income, {
                '80c': deduction_80c,
                '80d': deduction_80d,
                '80e': deduction_80e,
                '80eea': deduction_80eea,
                '80g': deduction_80g
            })
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

        happy_message = "Great news 🎉! You don't need to pay any tax this year!" if not suggestions else None

        # Context to pass to the template
        context = {
            'tax_old_regime': tax_old_regime if selected_scheme in ['both', 'old'] else None,
            'tax_new_regime': tax_new_regime if selected_scheme in ['both', 'new'] else None,
            'best_regime': best_regime,
            'suggestions': suggestions,
            'happy_message': happy_message,
            'user_name': request.user.username,
            'age_slab': age_slab,
            'standard_deduction_old': standard_deduction_old,
            'standard_deduction_new': standard_deduction_new,
            'thank_you_message': "Thank you for using TaxMaster!"
        }

        # Load the PDF template
        template = get_template('calculator/pdf_results.html')
        html = template.render(context)

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Tax_Calculation_Results.pdf"'

        # Generate PDF
        log_it("pdf generated")
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return HttpResponseBadRequest("Invalid request")


############################# Tax Slabs View ####################################################### 

def tax_slabs_view(request):
    return render(request, 'calculator/tax_slabs.html')
