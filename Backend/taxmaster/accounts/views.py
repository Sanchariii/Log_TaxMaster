import random
from django.views import View
from datetime import timedelta
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model,logout,authenticate, login as auth_login
from .forms import UsernamePasswordResetForm, OTPForm, SetNewPasswordForm
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import SignUpForm, UsernamePasswordResetForm, OTPForm, SetNewPasswordForm, LoginForm, GroupSelectionForm

#########################################################################################################
# from taxmaster.logging_config import logger
from logs.logging_config import logger

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

#########################################################################################################
@login_required
def check_session(request):
    return JsonResponse({'status': 'ok'})



############################# Dividing Groups #########################################################
def is_taxadvisor(user):
    return user.groups.filter(name='TaxAdvisor').exists()
def is_indivual_user(user):
    return user.groups.filter(name='Individual User').exists()
def is_User_or_Advisor(user):
    return is_taxadvisor(user) or is_indivual_user(user)
def is_Admin(user):
    return user.is_superuser


############################# Built-In Django View ######################################################
class CustomLoginView(View):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    otp_template_name = 'accounts/otp.html'

    def get(self, request):
        if 'otp_verified' in request.session and request.session['otp_verified']:
            return self._redirect_user(request.user)

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def render_error(self, form=None, error_message=None, template=None):
        """Render form with error message."""
        print(f"Error Message: {error_message}")  # Debugging line

        context = {'form': form} if form else {}
        if error_message:
            context['error_message'] = error_message
        template = template if template else self.template_name
        return render(self.request, template, context)

    def post(self, request):
        # Check if OTP has been sent
        if 'otp_sent' in request.session and request.session['otp_sent']:
            if 'resend_otp' in request.POST:
                # Logic to resend OTP
                new_otp = self.generate_otp()
                user_email = request.session.get('email')  # Retrieve email from session
                if user_email:
                    self.send_otp_via_email(user_email, new_otp)
                    request.session['otp'] = new_otp
                    request.session.modified = True  # Mark the session as modified
                    return render(request, self.otp_template_name, {'message': 'A new OTP has been sent to your email.'})
                else:
                    return self.render_error(error_message="Email not found in session.", template=self.otp_template_name)

            otp = request.POST.get('otp')
            if otp and otp == request.session.get('otp'):
                log_it("login successful")
                user = authenticate(username=request.session.pop('username'), password=request.session.pop('password'))
                if user:
                    auth_login(request, user)
                    request.session.pop('otp_sent', None)
                    request.session['otp_verified'] = True
                    return self._redirect_user(user)
                else:
                    return self.render_error(error_message="User authentication failed. Please try again.", template=self.otp_template_name)
            else:
                log_fail('login', 'Invalid OTP entered')
                return self.render_error(error_message="Invalid OTP. Please try again.", template=self.otp_template_name)

        
        # Process the login form
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            request.session['username'] = form.cleaned_data.get('username')
            request.session['password'] = form.cleaned_data.get('password')
            request.session['email'] = user.email  # Store email in session
            otp = self.generate_otp()
            request.session['otp'] = otp
            request.session['otp_sent'] = True
            self.send_otp_via_email(user.email, otp)
            return render(request, self.otp_template_name)
        else:
            log_fail('login', 'Invalid form submission')
            print(form.errors)  # Debugging line for form errors

            return self.render_error(form=form)


    def _redirect_user(self, user):
        """Redirects user based on their group."""
        if user.is_superuser:
            next_url = '/calculator/'
        elif user.groups.filter(name='Tax Advisor').exists():
            next_url = '/advisor/advisor-requests/'
        elif user.groups.filter(name='Individual User').exists():
            next_url = '/calculator/'
        else:
            next_url = '/calculator/'
        return redirect(next_url)

    def generate_otp(self):
        """Generates a 6-digit OTP."""
        log_it("otp sent")
        return str(random.randint(100000, 999999))

    def send_otp_via_email(self, email, otp):
        """Sends OTP to the given email."""
        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp}'
        from_email = 'raysanchari930@gmail.com'
        send_mail(subject, message, from_email, [email], fail_silently=False)

############################# Dividing Groups #########################################################
def group_selection(request):
    if request.method == 'POST':
        form = GroupSelectionForm(request.POST)
        if form.is_valid():
            selected_group = form.cleaned_data['group']
            user = request.user
            user.groups.clear()  # Clear any existing groups
            selected_group.user_set.add(user)  # Add the user to the selected group

            # Redirect based on the group the user selected
            if selected_group.name == 'Tax Advisor':
                log_registration('tax advisor')
                return redirect('tax_advisor_profile', user_id=user.id)
            elif selected_group.name == 'Individual User':
                log_registration('user')
                return redirect('tax_calculator')
    else:
        form = GroupSelectionForm()

    return render(request, 'accounts/group_selection.html', {'form': form})



############################# Signup ######################################################
User = get_user_model()

def generate_otp():
    """Generates a random 6-digit OTP."""
    log_it("otp sent")
    return ''.join(random.choices(string.digits, k=6))

def send_otp_via_email(email, otp):
    """Sends OTP to the given email."""
    subject = 'Your OTP for Account Verification'
    message = f'Your OTP code is {otp}'
    from_email = 'raysanchari930@gmail.com'
    send_mail(subject, message, from_email, [email], fail_silently=False)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists.')
                log_fail('signup','A user with this email already exists')
            else:
                # Generate OTP and send it to the user's email
                otp = generate_otp()
                send_otp_via_email(email, otp)
                
                # Store user details and OTP in session
                request.session['signup_data'] = {
                    'username': form.cleaned_data.get('username'),
                    'email': email,
                    'first_name': form.cleaned_data.get('first_name'),
                    'last_name': form.cleaned_data.get('last_name'),
                    'password': form.cleaned_data.get('password1'),
                }
                request.session['otp'] = otp
                
                # Redirect to OTP verification page
                return redirect('verify_signup_otp')
        else:
            messages.error(request, 'Please correct the errors below.')
            log_fail('signup','Invalid form submission')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def resend_signup_otp(request):
    """View for resending the OTP during signup."""
    if request.method == 'POST':
        signup_data = request.session.get('signup_data')
        if signup_data:
            email = signup_data.get('email')
            if email:
                # Generate a new OTP and send it to the email
                new_otp = generate_otp()
                send_otp_via_email(email, new_otp)

                # Update the OTP in the session
                request.session['otp'] = new_otp

                # Display a message confirming that the OTP has been resent
                messages.success(request, 'A new OTP has been sent to your registered email.')
            else:
                messages.error(request, 'Unable to resend OTP. No email found.')
        else:
            messages.error(request, 'Unable to resend OTP. Signup data not found.')

        # Redirect back to the OTP verification page
        return redirect('verify_signup_otp')

    return redirect('signup')



def verify_signup_otp(request):
    """View for verifying the OTP after signup."""
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')
            stored_otp = request.session.get('otp')
            
            if entered_otp == stored_otp:
                # OTP is correct, proceed with account creation
                signup_data = request.session.get('signup_data')
                if signup_data:
                    user = User.objects.create_user(
                        username=signup_data['username'],
                        email=signup_data['email'],
                        first_name=signup_data['first_name'],
                        last_name=signup_data['last_name'],
                        password=signup_data['password']
                    )
                    auth_login(request, user)

                    # Clear session data after successful signup
                    if 'signup_data' in request.session:
                        del request.session['signup_data']
                    if 'otp' in request.session:
                        del request.session['otp']
                    
                    # Redirect to group selection page
                    return redirect('group_selection')
            else:
                form.add_error('otp', 'Invalid OTP. Please try again.')
                log_fail('signup','Invalid OTP entered')

    else:
        form = OTPForm()

    return render(request, 'accounts/verify_otp.html', {'form': form})

################################## Logout View ############################################################
@login_required
def logout_view(request):
    
    logout(request)
    return redirect("/")




from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from .forms import ForgotPasswordForm



################################## Forgot Password #########################################################
# View for requesting a password reset
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = ''.join(random.choices(string.digits, k=6))  # Generate a random 6-digit OTP
                log_it("otp sent")
                
                # Send OTP via email
                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                # Store OTP in session or database (for simplicity, using session here)
                request.session['otp'] = otp
                request.session['user_id'] = user.id
                
                return redirect('verify_otp')  # Redirect to OTP verification page
            except User.DoesNotExist:
                form.add_error('email', 'No account associated with this email.')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'accounts/forgot_password.html', {'form': form})






# ################################## OTP Validation #######################################################
# View for verifying the OTP
def verify_otp_view(request):
    if request.method == 'POST':
        if 'resend_otp' in request.POST:
            # Resend OTP logic
            try:
                user_id = request.session.get('user_id')
                if user_id is None:
                    print('otp_resend', 'User ID is not available in session.')
                    return render(request, 'accounts/otp.html', {'form': OTPForm(), 'error_message': 'User ID not found. Please try logging in again.'})
                
                email = User.objects.get(id=user_id).email
                otp = ''.join(random.choices(string.digits, k=6))  # Generate a new OTP
                send_mail(
                    'Your resent OTP for Password Reset',
                    f'Your new OTP is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                request.session['otp'] = otp  # Update the stored OTP in session

                log_it(f"OTP resent successfully to {email}.")
                return render(request, 'accounts/otp.html', {'form': OTPForm(), 'message': 'OTP has been resent.'})
            except User.DoesNotExist:
                log_fail('otp_resend', 'User does not exist in the database.')
                return render(request, 'accounts/otp.html', {'form': OTPForm(), 'error_message': 'User does not exist.'})
            except Exception as e:
                log_fail('otp_resend', f'Unexpected error occurred: {str(e)}')
                return render(request, 'accounts/otp.html', {'form': OTPForm(), 'error_message': 'An error occurred while resending the OTP. Please try again.'})

        otp_form = OTPForm(request.POST)
        if otp_form.is_valid():
            entered_otp = otp_form.cleaned_data['otp']
            if entered_otp == request.session.get('otp'):
                return redirect('set_new_password')  # Redirect to set new password page
            else:
                otp_form.add_error('otp', 'Invalid OTP. Please try again.')
                log_fail('otp_validation', 'Entered OTP is invalid.')
    else:
        otp_form = OTPForm()

    return render(request, 'accounts/otp.html', {'form': otp_form})




# ################################## Reset Password #########################################################
# View for setting a new password
def set_new_password_view(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            
            # Clear the session variables after resetting the password
            del request.session['otp']
            del request.session['user_id']
            
            return redirect('login')  # Redirect to login page after successful password reset
    else:
        form = SetNewPasswordForm()
    
    return render(request, 'accounts/set_new_password.html', {'form': form})


# ################################## THE-END #########################################################





