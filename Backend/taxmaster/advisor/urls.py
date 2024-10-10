from django.urls import path
from . import views

urlpatterns = [
    path('available-advisors-view/', views.available_advisors_view, name='available_advisors_view'),
]

