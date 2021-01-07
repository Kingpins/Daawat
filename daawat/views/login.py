from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import  check_password
from django.views import  View
from daawat.service.astra_service import *

class Login(View):
    return_url = None
    # checks for return-url by using middlewares
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    # Performs login functionality.
    def post(self , request):
        userEmail = ""
        userPassword = ""
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if astra_service.check_connection() == False:
            astra_service.connect()
        user = astra_service.get_user_by_email(email)
        for out in user:
            userEmail = out["email"]
            userPassword = out["password"]  

        hotelExists = astra_service.get_hotel_exits(email)
        if hotelExists:
            result = astra_service.get_hotel_by_email(email)
            for out in result:
                request.session['hotelid'] = str(out["hotel_id"])

        error_message = None
        if userEmail != "":
            flag = check_password(password, userPassword)
            if flag:
                request.session['user'] = userEmail
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    messages.success(request,'Successfully Logged In !!')
                    return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        
        return render(request, 'login.html', {'error': error_message})

# clear out the session, therby logout the user.
def logout(request):
    request.session.clear()
    return redirect('login')
