from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import  check_password
from django.views import  View
from cassandra.util import min_uuid_from_time
from datetime import datetime, timedelta
from daawat.util.data_type_util import uuid_from_string, format_timestamp
from daawat.model.foods import Foods
from daawat.service.astra_service import *
from daawat.service.firebase_service import storage

class Food(View):
    def get(self , request):
        return redirect('hotel')
        
    # inserting data into foods table of Astra Datastax database, after inserting the image into firebase storage.
    # finally redirecting to hotel.py
    def post(self , request):
        error_message = None
        userEmail = request.session["user"]
        hotel_id = request.session["hotelid"]

        now = datetime.utcnow()
        food_id = min_uuid_from_time(now)
        
        if astra_service.check_connection() == False:
            astra_service.connect()
        
        postData = request.POST
        food_name = postData.get('food_name')
        food_description = postData.get('food_description')
        food_price = int(postData.get('food_price'))
        category_name = postData.get('category_name')
        food_img_temp = request.FILES['food_img']
        storage_link = storage.child("FoodImage/"+hotel_id+"/"+food_name+".jpg").put(food_img_temp)
        if storage_link:
            food_img = storage.child("FoodImage/"+hotel_id+"/"+food_name+".jpg").get_url(None)
        else:
            error_message = "unable to add the image"

        food = Foods(food_id,food_name,food_price,food_description,food_img,userEmail,hotel_id,category_name)
        if not error_message:
            astra_service.create_new_food(food)
            messages.success(request,'Successfully added the '+food_name+' !!')
            return redirect('hotel')

        return redirect('hotel')

# delete the food from database
def delete_food(request):
    if request.method == "GET":
        return redirect("hotel")
    if request.method == "POST":      
        postData = request.POST
        food_id = postData.get('food_id')
        astra_service.delete_food(food_id)
        messages.success(request,'Successfully deleted the food item !!')
        return redirect('hotel')


def update_food(request):

    # get the respective food by food_id
    if request.method == "GET":
        data = {}
        food_id = request.GET.get("food_id")
        request.session["food_id"] = food_id
        result = astra_service.get_food_by_food_id(food_id)
        for out in result:
            data["value"] = out
        return render(request, 'update_food.html' , data)

    # update the food in database table 'foods'
    if request.method == "POST":
        error_message = None
        userEmail = request.session["user"]
        hotel_id = request.session["hotelid"]
        food_id = request.session["food_id"]
        postData = request.POST
        food_name = postData.get('food_name')
        food_description = postData.get('food_description')
        food_price = int(postData.get('food_price'))
        category_name = postData.get('category_name')
        food_img = ""
        food = Foods(food_id,food_name,food_price,food_description,food_img,userEmail,hotel_id,category_name)
        if not error_message:
            astra_service.update_food(food,food_id)
            messages.success(request,'Successfully updated the '+food_name+' !!')
            return redirect('hotel')
        return redirect('update_food')


        
