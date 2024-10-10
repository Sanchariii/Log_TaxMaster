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
from django.contrib.auth import logout,authenticate, login as auth_login
from .forms import UsernamePasswordResetForm, OTPForm, SetNewPasswordForm
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import SignUpForm, UsernamePasswordResetForm, OTPForm, SetNewPasswordForm, LoginForm, GroupSelectionForm



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

    def post(self, request):
        if 'otp_sent' in request.session and request.session['otp_sent']:
            otp = request.POST.get('otp')
            if otp and otp == request.session.get('otp'):
                user = authenticate(username=request.session['username'], password=request.session['password'])
                if user:
                    auth_login(request, user)
                    request.session['otp_verified'] = True
                    return self._redirect_user(user)
            # messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, self.otp_template_name)

        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            password = form.cleaned_data.get('password')
            try:
                validate_password(password, user)
            except ValidationError as e:
                form.add_error('password', e)
                return render(request, self.template_name, {'form': form})

            request.session['username'] = form.cleaned_data.get('username')
            request.session['password'] = form.cleaned_data.get('password')
            otp = self.generate_otp()
            request.session['otp'] = otp
            request.session['otp_sent'] = True
            self.send_otp_via_email(user.email, otp)
            # messages.info(request, 'An OTP has been sent to your email. Please enter it to continue.')
            return render(request, self.otp_template_name)
        else:
            messages.error(request, 'Invalid username or password.')

        return render(request, self.template_name, {'form': form})

    def _redirect_user(self, user):
        """Redirects user based on their group."""
        if user.is_superuser:
            next_url = '/calculator/'
        elif user.groups.filter(name='TaxAdvisor').exists():
            next_url = '/base/'
        elif user.groups.filter(name='Individual User').exists():
            next_url = '/base/'
        else:
            next_url = '/calculator/'
        return redirect(next_url)

    def generate_otp(self):
        """Generates a 6-digit OTP."""
        return str(random.randint(100000, 999999))

    def send_otp_via_email(self, email, otp):
        """Sends OTP to the given email."""
        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)


# ############################# Manager Dashboard ######################################################
# @login_required
# @user_passes_test(is_taxadvisor)
# def mngr_dashboard(request):
#     user_profile = request.user.userprofile
#     company_users = User.objects.filter(userprofile__company=user_profile.company)
#     staffs = company_users.filter(groups__name='Individual User')
#     account_managers = company_users.filter(groups__name='Account Manager')
    
#     context = {
#         'staffs': staffs,
#         'account_managers': account_managers,
#     }
#     print(account_managers)
#     return render(request, 'account/mngr_dashboard.html', context)


############################### Home Page ############################################################
@login_required
def home(request):
    return render(request, 'crm/dashboard.html')


############################# Dividing Groups #########################################################
@login_required
@user_passes_test(is_User_or_Advisor)
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'accounts/group_list.html', {'groups': groups})

@login_required
@user_passes_test(is_Admin)
def group_list_Admin(request):
    groups = Group.objects.all()
    return render(request, 'accounts/group_list.html', {'groups': groups})



############################# Signup ######################################################
User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Now safe to access cleaned_data
            
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                user = form.save(commit=False)
                password = form.cleaned_data.get('password1')
                user.set_password(password)  # Set the password
                user.save()  # Save the user instance
                
                username = form.cleaned_data.get('username')
            
                return redirect('user_details')  # Make sure user_details view is set up correctly
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

################################## Logout View ############################################################
@login_required
def logout_view(request):
    
    logout(request)
    return redirect("/")


################################## Forgot Password #########################################################
def forgot_password(request):
    if request.method == 'POST':
        form = UsernamePasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                subject = 'Password Reset Requested'
                otp = str(random.randint(100000, 999999))  
                otp_generated_at = timezone.now() 
                
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                    'otp': otp,
                })
                send_mail(subject, message, None, [user.email])
                
                request.session['reset_username'] = username
                request.session['otp'] = otp
                request.session['otp_generated_at'] = otp_generated_at.isoformat() 
                
                return redirect('verify_otp')
            except User.DoesNotExist:
                form.add_error('username', 'User with this username does not exist.')
    else:
        form = UsernamePasswordResetForm()
    
    return render(request, 'registration/forgot_password.html', {'form': form})


################################## OTP Validation #######################################################
def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp')
            otp_generated_at = request.session.get('otp_generated_at')

            if not otp_generated_at:
                return redirect('forgot_password')

            otp_generated_at = datetime.fromisoformat(otp_generated_at)
            now = timezone.now() 

            if now - otp_generated_at > timedelta(minutes=1):
                return redirect('forgot_password')
            elif entered_otp == stored_otp:
                return redirect('password_reset_confirm')
            else:
                form.add_error('otp', 'Invalid OTP. Please try again.')
    else:
        form = OTPForm()
        otp_generated_at = request.session.get('otp_generated_at')
        if otp_generated_at:
            otp_generated_at = datetime.fromisoformat(otp_generated_at)
            now = timezone.now()
            remaining_time = max(0, 60 - (now - otp_generated_at).total_seconds())
            if remaining_time == 0:
                return redirect('forgot_password')
        else:
            remaining_time = 0
    return render(request, 'registration/verify_otp.html', {'form': form, 'remaining_time': remaining_time})


################################## Reset Password #########################################################
def password_reset_confirm(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            username = request.session.get('reset_username')
            new_password = form.cleaned_data['new_password']
            try:
                validate_password(new_password)
            except ValidationError as e:
                form.add_error('new_password', e)
            else:
                try:
                    user = User.objects.get(username=username)
                    user.set_password(new_password)
                    user.save()
                   
                    messages.success(request, 'Password reset successfully.')
                    return redirect('login')
                except User.DoesNotExist:
                    form.add_error(None, 'Error resetting password. Please try again.')
    else:
        form = SetNewPasswordForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})



################################## THE-END #########################################################