# all the necessary imports
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib import messages
from django.views import  View
from cassandra.util import min_uuid_from_time
from datetime import datetime, timedelta
from daawat.model.hotels import Hotels
from daawat.model.generate_qr import Generate_QR
from daawat.service.astra_service import *
from daawat.service.firebase_service import storage
from daawat.service.qrcode_service import *
from daawat.util.generate_pdf import *
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
class Hotel(View):
    def get(self , request):
        data = {}
        userEmail = request.session['user']
        request.session['table_no'] = '1'
        if astra_service.check_connection() == False:
            astra_service.connect()
        
        hotelExists = astra_service.get_hotel_exits(userEmail)
        if hotelExists:
            result = astra_service.get_hotel_by_email(userEmail)
            for out in result:
                data["hotel_details"] = out
                request.session["hotel_id"] = out["hotel_id"]
                hotel_id = request.session["hotel_id"]

        categoryExists = astra_service.get_category_exits(userEmail)
        if categoryExists:
            result_category = astra_service.get_category_by_hotel_id(hotel_id)
            data["categories"] = list(result_category)
        
            result = astra_service.get_food_by_email(userEmail)
            data["products"] = result
        data['category_exists'] = categoryExists
        return render(request , 'hotel.html', data)

    def post(self , request):
        userEmail = str(request.session['user'])
        data = {}
        error_message = None
        categoryID = None
        categoryNameforDisplay = None
        categoryName = request.POST.get('categoryBtn')
        currentCategory = request.POST.get('currentCategory')

        hotelExists = astra_service.get_hotel_exits(userEmail)
        if hotelExists:
            result = astra_service.get_hotel_by_email(userEmail)
            for out in result:
                data["hotel_details"] = out
                request.session["hotel_id"] = out["hotel_id"]
                hotel_id = request.session["hotel_id"]
    
        if categoryName:
            categoryID = astra_service.get_category_id_by_category_name(categoryName)

        categoryExists = astra_service.get_category_exits(userEmail)
        if categoryExists:
            result_category = astra_service.get_category_by_hotel_id(hotel_id)
            data["categories"] = list(result_category)
        data['category_exists'] = categoryExists
        if categoryID:
            products = astra_service.get_food_by_category_name(categoryName)
            categoryNameforDisplay = categoryName
        else:
            products = astra_service.get_food_by_email(userEmail)

        data['currentCategory'] = currentCategory
        data['categoryNameforDisplay'] = categoryNameforDisplay
        data["products"] = products

        
        now = datetime.utcnow()
        hotel_id = min_uuid_from_time(now)
        postData = request.POST
        hotel_name = postData.get('hotel_name')
        hotel_bio = postData.get('hotel_bio')
        hotel_address = postData.get('hotel_address')
        hotel_phone = postData.get('hotel_phone')
        hotel_tables = postData.get('hotel_tables')
        if hotel_name:
            hotel_logo_temp = request.FILES['hotel_logo']
            storage_link = storage.child("hotelLogo/"+hotel_name+".jpg").put(hotel_logo_temp)
            if storage_link:
                hotel_logo = storage.child("hotelLogo/"+hotel_name+".jpg").get_url(None)
            else:
                error_message = "unable to add the logo"
                
            hotel = Hotels(hotel_id, hotel_name,hotel_bio,hotel_address,hotel_phone,hotel_tables,hotel_logo,userEmail)

            if not error_message:
                astra_service.create_new_hotel(hotel)
                messages.success(request,'Successfully created the hotel, Start creating your menu!')
                request.session['hotelid'] = str(hotel_id)
                return redirect('hotel')
            else:
                data = {
                    'error': error_message,
                    'values': value
                }
        return render(request, 'hotel.html', data)

def print_qr(request):
    if request.method == "GET":
        pass

    # This method is used to print the QR image, by creating a pdf of it.
    if request.method == "POST" :
        postData = request.POST
        image_url = postData.get('image_url')
        table_no = postData.get('table_no')
        template = get_template('qr_pdf.html')
        context = {
            "image_url":image_url,
            "table_no":table_no
        }
        html = template.render(context)
        pdf = render_to_pdf('qr_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "QRImage" 
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            render(request,"menu.html")
            redirect("generate_qr")
            return response
        return HttpResponse("Not found")

# This method handles all the operations performed in generate_qr.html page.
def generate_qr(request):

    # used to get the hotel and no. of tables information from database
    if request.method =="GET":
        data = {}
        tables = None
        tableList = []
        table_no = request.session['table_no'] 
        userEmail = request.session['user']
        
        hotelExists = astra_service.get_hotel_exits(userEmail)
        if hotelExists:
            result = astra_service.get_hotel_by_email(userEmail)
            for out in result:
                data["hotel_details"] = out
                tables = int(out["hotel_tables"])

        qr_exists_in_db = astra_service.get_generate_qr_exits(userEmail)
        if qr_exists_in_db:
            for out in qr_exists_in_db:
                if out["table_no"] == table_no:
                    data["qr_details"] = out
                    

        for i in range(1,tables+1):
            tableList.append(i)
        data["hotel_tables"] = tableList
        return render(request , 'generate_qr.html', data)
    
    # generating QR code, saving the image in firebase and finally saving data in generate_qr table.
    if request.method =="POST":
        data = {}
        error_message = None
        userEmail = request.session['user']
        postData = request.POST
        hotel_name = postData.get('hotel_name')
        hotel_id = postData.get('hotel_id')
        table_no = postData.get('table_no')
        qr_exists_in_db = astra_service.get_generate_qr_exits(userEmail)
        if qr_exists_in_db:
            for out in qr_exists_in_db:
                if out["table_no"] == table_no:
                    data["qr_details"] = out
                    request.session['table_no'] = table_no
                    return redirect("generate_qr")
 
        qr_string = "https://daawat-menu.herokuapp.com/"+hotel_id+"/"+table_no
        image_name = hotel_name+table_no
        GenerateQR(qr_string,image_name)
        path_of_storage = os.path.join(BASE_DIR,'qr_images')

        storage_link = storage.child("hotelQR/"+hotel_name+table_no+".jpg").put(path_of_storage+"/"+image_name+".png")
        if storage_link:
            qr_image = storage.child("hotelQR/"+hotel_name+table_no+".jpg").get_url(None)
        else:
            error_message = "unable to add the logo"
        
        generate_qr =  Generate_QR(hotel_name,hotel_id,userEmail,qr_image,table_no)
        astra_service.create_generate_qr(generate_qr)
        return redirect("generate_qr")
