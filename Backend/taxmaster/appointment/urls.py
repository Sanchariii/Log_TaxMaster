from django.urls import path
from . import views

urlpatterns = [
    path('check-availability/', views.check_availability, name='check_availability'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('available-dates/', views.available_dates_view, name='available_dates'),
    path('request-appointment/<int:advisor_id>/', views.request_appointment, name='request_appointment'),
]

