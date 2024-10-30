from django.core.management.base import BaseCommand
from calculator.models import TaxScheme, SurchargeRate

class Command(BaseCommand):
    help = 'Populate tax scheme and surcharge rate data'

    def handle(self, *args, **kwargs):
        # Populate TaxScheme data
        tax_schemes = [
            {'regime': 'old', 'slab': 'Upto ₹ 2.5 lakh', 'rate': 0},
            {'regime': 'old', 'slab': '₹ 2.5 lakh - ₹ 5 lakh', 'rate': 5},
            {'regime': 'old', 'slab': '₹ 5 lakh - ₹ 10 lakh', 'rate': 20},
            {'regime': 'old', 'slab': 'More than ₹ 10 lakh', 'rate': 30},
            {'regime': 'new', 'slab': 'Upto ₹ 3 lakh', 'rate': 0},
            {'regime': 'new', 'slab': '₹ 3 lakh - ₹ 7 lakh', 'rate': 5},
            {'regime': 'new', 'slab': '₹ 7 lakh - ₹ 10 lakh', 'rate': 10},
            {'regime': 'new', 'slab': '₹ 10 lakh - ₹ 12 lakh', 'rate': 15},
            {'regime': 'new', 'slab': '₹ 12 lakh - ₹ 15 lakh', 'rate': 20},
            {'regime': 'new', 'slab': 'More than ₹ 15 lakh', 'rate': 30},
        ]

        for scheme in tax_schemes:
            TaxScheme.objects.get_or_create(regime=scheme['regime'], slab=scheme['slab'], rate=scheme['rate'])

        # Populate SurchargeRate data
        surcharge_rates = [
            {'slab': 'Upto ₹ 50 lakh', 'rate': 0},
            {'slab': '₹ 50 lakh - ₹ 1 crore', 'rate': 10},
            {'slab': '₹ 1 crore - ₹ 2 crore', 'rate': 15},
            {'slab': '₹ 2 crore - ₹ 5 crore', 'rate': 25},
            {'slab': 'More than ₹ 5 crore', 'rate': 37},
        ]

        for rate in surcharge_rates:
            SurchargeRate.objects.get_or_create(slab=rate['slab'], rate=rate['rate'])

        self.stdout.write(self.style.SUCCESS('Successfully populated tax scheme and surcharge rate data'))
