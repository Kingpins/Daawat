from django.http import HttpResponse
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.views.generic import View
from django.core.paginator import Paginator
from daawat.util.generate_pdf import render_to_pdf 
from django.template.loader import get_template
from daawat.service.astra_service import *
from .menu import hotel_exists

class GeneratePDF(View):
    def post(self, request, *args, **kwargs):
        ordersList = []
        foodIds = []
        data = {}
        invoiceList = []
        
        hotel_id = request.session.get('hotelid')
        grand_total = request.POST.get('grand_total')
        invoice_id = request.POST.get('invoice_id')
        time_of_invoice = request.POST.get('time_of_invoice')
        hotel_exists(data,hotel_id)
        
        invoices = astra_service.get_invoice_by_invoice_id(invoice_id)
        for i in invoices:
            invoiceList.append(i)
            foodIds.append(i["product"])
        
        foodIds = set(foodIds)
        products = astra_service.get_food_by_food_ids(foodIds)
        
        
        template = get_template('invoice_admin.html')
        context = {
            "invoices": invoiceList,
            "invoice_id":invoice_id,
            "invoice_date":time_of_invoice,
            "data": data,
            "foods":products,
            "grand_total":grand_total,
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
            return response
        return HttpResponse("Not found")


    def get(self, request, *args, **kwargs):

        data = {}
        invoiceList = []
        invoice_numbers = []
        customer_info_list = []
        if astra_service.check_connection() == False:
            astra_service.connect()

        page = request.GET.get("page")
        hotel_id = request.session.get('hotelid')
        invoices = astra_service.get_invoice_by_hotel_id(hotel_id)

        for i in invoices:
            invoice_numbers.append(i["invoice_id"])

        invoice_numbers = set(invoice_numbers)

        for invoice_id in invoice_numbers:
            result = astra_service.get_invoice_by_invoice_id_with_limit_1(invoice_id)
            for out in result:
                invoiceList.append(out)
        invocieList = invoiceList.sort(key=lambda x:x["time_of_invoice"],reverse=True)


        p = Paginator(invoiceList,10)
        page_obj = p.get_page(page)
        
      
        data["invoices"] = page_obj
        data["invoice_numbers"] = invoice_numbers
        return render(request , 'invoice_details.html'  , data)