from django.urls import path
from .views import old_tax_scheme_view, new_tax_scheme_view, surcharge_tax_view,tax_calculator_view
urlpatterns = [
   path('', tax_calculator_view, name='tax_calculator'),
   path('old_tax_scheme/', old_tax_scheme_view, name='old_tax_scheme'),
   path('new_tax_scheme/', new_tax_scheme_view, name='new_tax_scheme'),
   path('surcharge_tax/', surcharge_tax_view, name='surcharge_tax'),
#    path('print-pdf/', print_pdf_view, name='print_pdf'),
]