from django.urls import path
from .views import (
    # check_session,
    CustomLoginView,
    # home,
    # group_list,
    # group_list_Admin,
    signup,
    logout_view,
    # forgot_password,
    # verify_otp,
    # password_reset_confirm,
    forgot_password_view,
    verify_otp_view,
    verify_signup_otp,
    set_new_password_view,
    group_selection
)

urlpatterns = [
    # path('check_session/', check_session, name='check_session'),#NE
    path('login/', CustomLoginView.as_view(), name='login'),
    # path('home/', home, name='home'),
    # path('groups/', group_list, name='group_list'),#NE
    # path('groups/admin/', group_list_Admin, name='group_list_Admin'),#NE
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    # path('forgot_password/', forgot_password, name='forgot_password'),#to be done
    # path('verify_otp/', verify_otp, name='verify_otp'),
    # path('password_reset_confirm/', password_reset_confirm, name='password_reset_confirm'),#to be done
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('set-new-password/', set_new_password_view, name='set_new_password'),
    path('group-selection/', group_selection, name='group_selection'),
    path('verify-signup-otp/', verify_signup_otp, name='verify_signup_otp')
]