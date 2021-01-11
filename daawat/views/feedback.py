from django.shortcuts import render , redirect, HttpResponse
from django.contrib import messages
from django.views import  View
from daawat.service.astra_service import *

class Feedback(View):

    def post(self , request):
            pass

    def get(self , request):
        data = {}
        feedbackList = []
        sum = 0
        hotel_id = request.session["hotelid"]
        feedbacks = astra_service.get_feedbacks_by_hotel_id(hotel_id)
        for out in feedbacks:
            feedbackList.append(out)
        for a in feedbackList:
            sum += float(a["ratings"])
        starRatings = round(sum/len(feedbackList),1)
        data["feedback"] = {"ratings":str(starRatings)}
        data["feedbacks"] = feedbackList
        return render(request , 'feedback.html' , data )

