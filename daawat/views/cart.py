from django.shortcuts import render , redirect, HttpResponse
from django.contrib import messages
from django.views import  View
from cassandra.util import min_uuid_from_time
from datetime import datetime, timedelta
from daawat.model.foods import Foods
from daawat.service.astra_service import *
from .menu import hotel_exists

class Cart(View):

    # adds product to cart, which is a session variable.
    def post(self , request):
            data = {}
            hotel_id = request.session["hotel_id"]
            hotel_exists(data,hotel_id)
            product = request.POST.get('product')
            remove = request.POST.get('remove')
            cart = request.session.get('cart')
            if cart:
                quantity = cart.get(product)
                if quantity:
                    if remove:
                        if quantity<=1:
                            cart.pop(product)
                            messages.warning(request,'Item is removed from cart!')
                        else:
                            cart[product]  = quantity-1
                            messages.warning(request,'Item quantity is deducted from cart!')
                    else:
                        cart[product]  = quantity+1
                        messages.success(request,'Item quantity is updated in cart!')
                else:
                    cart[product] = 1
            else:
                cart = {}
                cart[product] = 1

            request.session['cart'] = cart 
            return redirect('cart')

    # checks if the hotel_id exists, then display all the products in cart.
    def get(self , request):
        data = {}
        if "hotel_id" not in request.session :
            return HttpResponse("Thank You, Visit Again")
        hotel_id = request.session["hotel_id"]
        hotel_exists(data,hotel_id)
        ids = list(request.session.get('cart').keys())
        products = astra_service.get_food_by_food_ids(ids)
        data["products"] = products
        return render(request , 'cart.html' , data )

