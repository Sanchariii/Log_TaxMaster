from django.urls import path
from .views import dashboard, home_view, user_appointments_view

urlpatterns = [
    path('dashboard', dashboard, name = 'dashboard'),
    path('', home_view, name='home'),
    path('user-appointments/', user_appointments_view, name='user_appointments'),
    # path('user-details/', user_details_view, name='user_details'),
]
