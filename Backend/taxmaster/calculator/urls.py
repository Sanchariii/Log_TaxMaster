from django.urls import path
from .views import tax_calculator_view,tax_slabs_view, tax_calculator_pdf_view, past_calculations_view
urlpatterns = [
   path('', tax_calculator_view, name='tax_calculator'),
   path('tax-slabs/', tax_slabs_view, name='tax_slabs'),
   path('tax-calculator/pdf/', tax_calculator_pdf_view, name='tax_calculator_pdf'),
   path('past-calculations/', past_calculations_view, name='past_calculations'),
]