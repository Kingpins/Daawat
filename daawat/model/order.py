from daawat.util.data_type_util import uuid_from_string, format_timestamp
from datetime import datetime

# Orders model, for orders table
class Orders(object):
    def __init__(self, customer_id, hotel_id, order_id, product,time_of_order,price,quantity):
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.order_id = str(order_id)
        self.product_id = product
        self.time_of_order = datetime.timestamp(time_of_order)
        self.price = price
        self.quantity = str(quantity)
    
    