from daawat.util.data_type_util import uuid_from_string, format_timestamp
# Categorys model, for categorys table
class Categorys(object):
    def __init__(self, category_id, category_img,category_name,userEmail,hotel_id):
        self.category_id = str(uuid_from_string(category_id))
        self.category_img = category_img
        self.category_name = category_name
        self.userEmail = userEmail
        self.hotel_id = hotel_id
    
    