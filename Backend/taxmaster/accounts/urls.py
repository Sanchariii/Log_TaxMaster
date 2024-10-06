from django.urls import path
from .views import (
    check_session,
    CustomLoginView,
    home,
    group_list,
    group_list_Admin,
    signup,
    logout_view,
    forgot_password,
    verify_otp,
    password_reset_confirm,
)

urlpatterns = [
    path('check_session/', check_session, name='check_session'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('home/', home, name='home'),
    path('groups/', group_list, name='group_list'),
    path('groups/admin/', group_list_Admin, name='group_list_Admin'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout_view'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('password_reset_confirm/', password_reset_confirm, name='password_reset_confirm'),
]