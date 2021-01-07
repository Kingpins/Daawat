from django.http import HttpResponse
from django.views.generic import View
from daawat.util.generate_pdf import render_to_pdf 
from django.template.loader import get_template


class GeneratePDF(View):
    def post(self, request, *args, **kwargs):
        orderId = request.POST.get("orderId")
        orders = Order.get_allorders_by_orderid(orderId)
        get_Single_Order = Order.get_allorders_by_order_id(orderId)
        template = get_template('invoice.html')
        context = {
            "orderId": orderId,
            "orders": orders,
            "singleOrder" : get_Single_Order
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s" %(orderId)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

    def get(self, request, *args, **kwargs):
        orderId = request.POST.get("orderId")
        orders = Order.get_allorders_by_orderid(orderId)
        get_Single_Order = Order.get_allorders_by_order_id(orderId)
        template = get_template('invoice.html')
        context = {
            "orderId": orderId,
            "orders": orders,
            "singleOrder" : get_Single_Order
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s" %(orderId)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")