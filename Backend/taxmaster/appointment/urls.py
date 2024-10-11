from django.urls import path
from . import views

urlpatterns = [
    path('check-availability/', views.check_availability, name='check_availability'),#NE
    path('book-appointment/', views.book_appointment, name='book_appointment'),#NE
    path('available-dates/', views.available_dates_view, name='available_dates'),#NE
    path('request-appointment/<int:advisor_id>/', views.request_appointment, name='request_appointment'),
    path('request-already-submitted/', views.appointment_request_sent, name='appointment_request_already_submitted'),
    path('approved/', views.approved_requests, name='approved_requests'),
    path('appointment_request_sent/', views.appointment_request_sent, name='appointment_request_sent')
]

