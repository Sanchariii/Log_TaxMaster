from django.urls import path
from .views import user_details_view, old_tax_scheme_view, new_tax_scheme_view, surcharge_tax_view

urlpatterns = [
    path('', user_details_view, name='user_details'),
    path('old_tax_scheme/', old_tax_scheme_view, name='old_tax_scheme'),
    path('new_tax_scheme/', new_tax_scheme_view, name='new_tax_scheme'),
    path('surcharge_tax/', surcharge_tax_view, name='surcharge_tax'),
]
