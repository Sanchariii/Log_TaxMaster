from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password


class GroupSelectionForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select Group", required=True)

# class GroupForm(forms.ModelForm):
#     class Meta:
#         model = Group
#         fields = ['name']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    username = forms.CharField(max_length=150, required=True, help_text='Required. Enter a username.')
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Required. Enter a password.')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Required. Enter the same password again for verification.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError('First name must contain only letters.')
        if not first_name.isupper():
            raise forms.ValidationError('First name must start with a capital letter.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must contain only letters.')
        if not last_name.isupper():
            raise forms.ValidationError('Last name must start with a capital letter.')
        return last_name

    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

##################################          ###############################################
class UsernamePasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Username')


##################################          ###############################################
class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label='OTP')


##################################          ################################################
class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

##################################          #################################################