from django.shortcuts import render , redirect , HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from daawat.service.astra_service import astra_service

class Index(View):

    def post(self , request):           
            pass

    def get(self , request):
        # connect astra datastax cloud cql database
        try:
            resp = astra_service.connect()
            print(resp)
        except:
            HttpResponse("Unable to connect cloud, Please try reloading.")
        
        return render(request,"home.html")
