from django.urls import path
from .views import (
    
    CustomLoginView,
    signup,
    logout_view,
    forgot_password_view,
    verify_otp_view,
    verify_signup_otp,
    set_new_password_view,
    group_selection,
    resend_signup_otp,
)

urlpatterns = [
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('set-new-password/', set_new_password_view, name='set_new_password'),
    path('group-selection/', group_selection, name='group_selection'),
    path('verify-signup-otp/', verify_signup_otp, name='verify_signup_otp'),
    path('resend-signup-otp/', resend_signup_otp, name='resend_signup_otp'),
]