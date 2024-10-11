from django.urls import path
from . import views
import appointment.views as av

urlpatterns = [
    path('available-advisors-view/', views.available_advisors_view, name='available_advisors_view'),
    path('advisor-requests/', views.advisor_requests, name='advisor_requests'),
    path('approve-request/<int:request_id>/', av.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', av.reject_request, name='reject_request'),
    path('manage-requests/', av.manage_requests_view, name='manage_requests'),#not working
]


