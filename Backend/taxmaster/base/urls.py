from django.urls import path
from .views import dashboard, home_view, user_appointments_view, learn_more, how_our_site_works

urlpatterns = [
    path('dashboard', dashboard, name = 'dashboard'),
    path('', home_view, name='home'),
    path('user-appointments/', user_appointments_view, name='user_appointments'),
    path('learn-more/', learn_more, name='learn_more'),
    path('how-our-site-works/', how_our_site_works, name='how_our_site_works'),
]
