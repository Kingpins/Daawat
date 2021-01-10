from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)

@register.filter(name='change_to_date')
def change_to_date(timestamp):
    return datetime.fromtimestamp(timestamp)

@register.filter(name='no_orders_pending')
def no_orders_pending(customer_id,orders):
    count = 0
    for order in orders:
        if order["customer_id"] == customer_id:
            if order["status"] == False:
                count += 1
    return count

@register.filter(name='multiply')
def multiply(number , number1):
    return int(number) * int(number1)

@register.filter(name='counter')
def count(val):
    return int(val + 1)
