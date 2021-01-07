from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)

@register.filter(name='change_to_date')
def change_to_date(timestamp):
    return datetime.fromtimestamp(timestamp)


@register.filter(name='multiply')
def multiply(number , number1):
    return int(number) * int(number1)

@register.filter(name='counter')
def count(val):
    return int(val + 1)
