from django.urls import path,include
from . import views


urlpatterns = [
    path('request-appointment/<int:advisor_id>/', views.request_appointment, name='request_appointment'),
    path('request-already-submitted/', views.appointment_request_sent, name='appointment_request_already_submitted'),
    path('approved/', views.approved_requests, name='approved_requests'),
    path('appointment_request_sent/', views.appointment_request_sent, name='appointment_request_sent'),
    path('my-appointments/', views.user_appointments, name='user_appointments'),
    path('calculator/', include('calculator.urls')),
]

