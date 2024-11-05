from django import template
from django.utils.translation import gettext as _

register = template.Library()

@register.filter(name='currency_format')
def currency_format(value):
    """
    Formats a number as currency (e.g., ₹1,000.00).
    
    Usage:
        {{ value|currency_format }}
    """
    if value is None:
        return _("N/A")
    try:
        return f"₹{value:,.2f}"
    except (ValueError, TypeError):
        return _("Invalid value")

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Adds a CSS class to a form field widget.

    Usage:
        {{ form.field_name|add_class:"my-css-class" }}
    """
    return field.as_widget(attrs={"class": css_class})
