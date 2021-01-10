from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib import messages
from django.views import  View
from cassandra.util import min_uuid_from_time
from datetime import datetime, timedelta
from daawat.model.hotels import Hotels
from daawat.model.customer import Customers
from daawat.service.astra_service import *
from django.http import HttpResponse
from daawat.service.speak_service import *
from daawat.service.firebase_service import *

class Menu(View):
    def get(self , request, hotel_id, table_no):
        data = {}
        request.session["hotel_id"] = hotel_id
        request.session["table_no"] = table_no
        tableList = []
        tables = None
        try:
            if astra_service.check_connection() == False:
                astra_service.connect()
        except:
            HttpResponse("Unable to connect cloud, Please try reloading.")

        hotelExists = astra_service.get_hotel_exits_by_hotel_id(hotel_id)
        if hotelExists:
            result = astra_service.get_hotel_by_hotel_id(hotel_id)
            for out in result:
                data["hotel_details"] = out
                HotelName = out["hotel_name"]
                data["hotel_exists"] = True
                tables = int(out["hotel_tables"])
            for i in range(1,tables+1):
                tableList.append(i)
            if int(table_no) not in tableList:
                data["hotel_exists"] = False
            audio_link = storage.child("hotelAudioClips/"+HotelName+".mp3").get_url(None)
            data["music"] = audio_link
        else:
            data["hotel_exists"] = False
    
        return render(request , 'customer_info.html',data)

    def post(self , request):
        pass


def hotel_exists(data,hotel_id):
    hotelExists = astra_service.get_hotel_exits_by_hotel_id(hotel_id)
    if hotelExists:
        result = astra_service.get_hotel_by_hotel_id(hotel_id)
        for out in result:
            data["hotel_details"] = out
            data["hotel_exists"] = True
            HotelName = out["hotel_name"]
    return data,HotelName


def add_customer(request):
    if request.method =="GET":
        data = {}
        if "customer_id" not in request.session :
            return HttpResponse("This is either trespassing or you could have completed the dining, Thank You, Visit Again")
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        hotel_id = request.session["hotel_id"] 
        table_no = request.session["table_no"] 
        data,HotelName = hotel_exists(data,hotel_id)
        customer_id = request.session["customer_id"] 
        if customer_id != None:
            customer_status = astra_service.customer_status_by_customer_id(customer_id)
            for out in customer_status:
                if out["status"] == True:
                    result_category = astra_service.get_category_by_hotel_id(hotel_id)
                    data["categories"] = result_category
                    ids = list(request.session.get('cart').keys())
                    if len(ids) == 0:
                        data["music"] = storage_link = storage.child("hotelAudioClips/"+HotelName+"Categories.mp3").get_url(None) 
                    return render(request , 'menu.html',data)
                else:
                    return render(request , 'loading.html',data)
            
        return render(request,'loading.html',data)

    if request.method =="POST":
        data = {}
        error_message = None
        postData = request.POST
        now = datetime.utcnow()
        customer_id = min_uuid_from_time(now)
        customer_name = postData.get('customer_name')
        request.session["customer_name"] = customer_name
        hotel_id = request.session["hotel_id"]
        table_no = request.session["table_no"]
        status = False
        customer =  Customers(customer_id,customer_name,status,hotel_id,table_no)
        astra_service.create_new_customer(customer)
        request.session["customer_id"] = customer.customer_id
        return render (request,"loading.html")

def main_menu(request):
    if request.method =="GET":
        data = {}
        if "customer_id" not in request.session :
            return HttpResponse("This is either trespassing or you could have completed the dining, Thank You, Visit Again")
        hotel_id = request.session["hotel_id"] 
        hotel_exists(data,hotel_id)
        category_name = request.session["category_name"] 
        result = astra_service.get_food_by_category_name(category_name)
        data["foods"] = result
        return render(request, 'menu_items.html',data) 
    if request.method =="POST":
        data = {}
        hotel_id = request.session["hotel_id"] 
        hotel_exists(data,hotel_id)
        category_name = request.POST.get("category_name")
        request.session["category_name"] = category_name
        result = astra_service.get_food_by_category_name(category_name)
        data["foods"] = result
        return render(request, 'menu_items.html',data) 

def main_items(request):
    if request.method =="GET":
        data = {}
        foodList = []
        hotel_id = request.session["hotel_id"] 
        hotel_exists(data,hotel_id)
        if "category_name" not in request.session :
            return HttpResponse("This is either trespassing or you could have completed the dining, Thank You, Visit Again")
        category_name = request.session["category_name"] 
        result = astra_service.get_food_by_category_name(category_name)
        for out in result:
            foodList.append(out)
        data["foods"] = foodList
        return render(request, 'menu_items.html',data) 
    if request.method =="POST":
        data = {}
        hotel_id = request.session["hotel_id"] 
        hotel_exists(data,hotel_id)
        category_name = request.session["category_name"] 
        result = astra_service.get_food_by_category_name(category_name)
        data["foods"] = result

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
                messages.success(request,'Item is added to cart!')
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return render(request, 'menu_items.html',data) 

def loading(request):
    if request.method =="GET":
        customer_id = request.session["customer_id"] 
        if customer_id != None:
            customer_status = astra_service.customer_status_by_customer_id(customer_id)
            for out in customer_status:
                if out["status"] == True:
                    return render(request , 'menu.html')
                else:
                    return render(request , 'loading.html')
        return render(request,'loading.html')
    if request.method =="POST":
        pass