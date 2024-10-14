from django.urls import path
from .views import tax_calculator_view,tax_slabs_view, tax_calculator_pdf_view
urlpatterns = [
   path('', tax_calculator_view, name='tax_calculator'),
   path('tax-slabs/', tax_slabs_view, name='tax_slabs'),
   path('tax-calculator/pdf/', tax_calculator_pdf_view, name='tax_calculator_pdf'),

   # path('old_tax_scheme/', old_tax_scheme_view, name='old_tax_scheme'),
   # path('new_tax_scheme/', new_tax_scheme_view, name='new_tax_scheme'),
   # path('surcharge_tax/', surcharge_tax_view, name='surcharge_tax'),
#    path('print-pdf/', print_pdf_view, name='print_pdf'),
]