from daawat.util.data_type_util import uuid_from_string, format_timestamp
# Customers model, for customers table
class Customers(object):
    def __init__(self,customer_id, customer_name,status,hotel_id,table_no):
        self.customer_id = str(uuid_from_string(customer_id))
        self.customer_name = customer_name
        self.status = status
        self.hotel_id = hotel_id
        self.table_no = table_no
    
    