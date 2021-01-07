from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from daawat.service.astra_service import *
from cassandra.util import min_uuid_from_time
from daawat.model.order import Orders
from daawat.model.inovice import Invoices
from datetime import datetime, timedelta
from .menu import hotel_exists
import random
from daawat.util.generate_pdf import *

class PlaceOrder(View):
    def post(self, request):
        hotel_id = request.session.get('hotel_id')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = astra_service.get_food_by_food_ids(list(cart.keys()))
        error_message = None
        
        if not error_message:
            for product in products:
                order_id = random.randint(1,10000000)
                order = Orders(customer_id = customer,
                          hotel_id = hotel_id,
                          order_id = order_id,
                          time_of_order = datetime.now(),
                          price=product["food_price"],
                          quantity=cart.get(product["food_id"]),
                          product=product["food_id"]
                          )
                astra_service.create_order(order)
                
            request.session['cart'] = {}
            messages.success(request,"Order placed successfully!")
            return redirect('cart')
        else:
            messages.warning(request,error_message)
            return redirect('cart')

def create_invoice(request):
    if request.method =="GET":
        pass
    if request.method =="POST":
        hotel_id = request.session.get('hotel_id')
        customer_id = request.session.get('customer_id')
        grand_total = request.POST.get('grand_total')
        ordersList = []
        data = {}
        customer_ids = []
        foodIds = []
        hotel_exists(data,hotel_id)
        customer_ids.append(customer_id)
        orders = astra_service.get_order(hotel_id,customer_ids)
        for out in orders:
            ordersList.append(out)
            foodIds.append(out["product"])
        
        foodIds = set(foodIds)
        products = astra_service.get_food_by_food_ids(foodIds)
        invoice_id = random.randint(1,10000000)
        time_of_invoice = datetime.now()
        for result in ordersList:
            invoice = Invoices(customer_id = result["customer_id"],
                          hotel_id = result["hotel_id"],
                          order_id = result["order_id"],
                          invoice_id = invoice_id,
                          time_of_invoice = time_of_invoice,
                          price=result["price"],
                          quantity=result["quantity"],
                          product=result["product"],
                          grand_total = grand_total,
                          )
            astra_service.create_invoice(invoice)
        
        invoiceList = []
        customer_info_list = []
        invoices = astra_service.get_invoice_by_invoice_id(str(invoice_id))
        customer_info = astra_service.get_customer_by_customer_id(customer_id)
        for c in customer_info:
            customer_info_list.append(c)
        for i in invoices:
            invoiceList.append(i)

        template = get_template('invoice.html')
        context = {
            "invoices": invoiceList,
            "invoice_id":invoice_id,
            "invoice_date":time_of_invoice,
            "data": data,
            "foods":products,
            "grand_total":grand_total,
            "customer":customer_info_list
        }
        
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s" %(invoice_id)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            request.session.clear()
            render(request,"menu.html")
            return response
        return HttpResponse("Not found")

        
        


