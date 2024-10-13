from django.urls import path
from .views import UserCreate

urlpatterns = [
    path('api/register/', UserCreate.as_view(), name='api-register'),
]
