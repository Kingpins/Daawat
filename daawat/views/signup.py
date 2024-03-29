from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.views import View
from django.contrib import messages
from daawat.model.users import Users
from daawat.service.astra_service import *

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')
        

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        user = Users(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateUser(user)

        if not error_message:
            user.password = make_password(user.password)
            if astra_service.check_connection() == False:
                astra_service.connect()
            astra_service.create_new_user(user.first_name, user.last_name, user.phone, user.email, user.password)
            messages.success(request,'Successfully created the account, Go to Login!')
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateUser(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10 or len(customer.phone) > 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif astra_service.get_user_exits(customer.email):
            error_message = 'Email Address Already Registered..'

        return error_message
