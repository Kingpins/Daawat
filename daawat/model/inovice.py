from daawat.util.data_type_util import uuid_from_string, format_timestamp
from datetime import datetime

# Invoices model, for invoices table
class Invoices(object):
    def __init__(self, customer_id, hotel_id, order_id,invoice_id, product,time_of_invoice,price,quantity,grand_total):
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.order_id = order_id
        self.invoice_id = str(invoice_id)
        self.product_id = product
        self.price = str(price)
        self.quantity = quantity
        self.time_of_invoice =datetime.timestamp( time_of_invoice)
        self.grand_total = str(grand_total)
    
    