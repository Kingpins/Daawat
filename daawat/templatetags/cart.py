from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(food  , cart):
    keys = cart.keys()
    for id in keys:
        if id == food["food_id"]:
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(food  , cart):
    keys = cart.keys()
    for id in keys:
        if id == food["food_id"]:
            return cart.get(id)
    return 0

@register.filter(name='price_total')
def price_total(food  , cart):
    return food["food_price"] * cart_quantity(food , cart)

@register.filter(name='price_total_in_order')
def price_total_in_order(food_price  , quantity):
    return int(food_price) * int(quantity)

@register.filter(name='total_cart_price')
def total_cart_price(foods , cart):
    sum = 0 
    for p in foods:
        sum += price_total(p , cart)
    return sum

@register.filter(name='total_order_price')
def total_order_price(orders):
    sum = 0 
    for p in orders:
        sum += price_total_in_order(p["price"] , p['quantity'])
    return sum
