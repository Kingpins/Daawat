from django.shortcuts import render , redirect, HttpResponse
from django.contrib import messages
from django.views import  View
from cassandra.util import min_uuid_from_time
from datetime import datetime, timedelta
from daawat.service.astra_service import *
from .menu import hotel_exists

class MakeBill(View):
    def post(self , request):
        pass    
    
    def get(self , request):
        foodIds = []
        ordersList = []
        data = {}
        customer_ids = []
        if "hotel_id" not in request.session :
            return HttpResponse("This is either trespassing or you could have completed the dining, Thank You, Visit Again")
        hotel_id = request.session["hotel_id"] 
        hotel_exists(data,hotel_id)
        customer_id = request.session["customer_id"] 
        customer_ids.append(customer_id)
        orders = astra_service.get_order(hotel_id,customer_ids)
        for out in orders:
            foodIds.append(out["product"])
            ordersList.append(out)
        foodIds = set(foodIds)

        products = astra_service.get_food_by_food_ids(foodIds)

        data["allow_bill"] = False
        count = 0
        for result in ordersList:
            if result['status'] == True:
                count += 1

        if count == len(ordersList):
            data["allow_bill"] = True
        data["orders"] = ordersList
        data["products"] = products
        return render(request , 'makebill.html' , data )
