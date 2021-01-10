from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import  check_password
from django.views import  View
from cassandra.util import min_uuid_from_time
from datetime import datetime, timedelta
from daawat.service.firebase_service import *
from daawat.model.categorys import Categorys
from daawat.service.astra_service import *

class Category(View):
    # redirecting to GET method of Hotel class in hotel.py
    def get(self , request):
        return redirect('hotel')

    # inserting data into categorys table of Astra Datastax database, after inserting the image into firebase storage.
    # finally redirecting to hotel.py
    def post(self , request):
        error_message =None
        userEmail = request.session["user"]
        hotel_id = request.session["hotelid"]

        now = datetime.utcnow()
        category_id = min_uuid_from_time(now)
        
        if astra_service.check_connection() == False:
            astra_service.connect()
        
        postData = request.POST
        category_name = postData.get('category_name')
        category_img_temp = request.FILES['category_img']
        storage_link = storage.child("CategoryImage/"+hotel_id+"/"+category_name+".jpg").put(category_img_temp)
        if storage_link:
            category_img = storage.child("CategoryImage/"+hotel_id+"/"+category_name+".jpg").get_url(None)
        else:
            error_message = "unable to add the image"
        category = Categorys(category_id,category_img,category_name,userEmail,hotel_id)
        astra_service.create_new_category(category)
        messages.success(request,'Successfully added the '+category_name+' category !!')
        return redirect('hotel')
       
