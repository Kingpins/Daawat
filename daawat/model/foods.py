from daawat.util.data_type_util import uuid_from_string, format_timestamp
# Foods model, for foods table
class Foods(object):
    def __init__(self, food_id, food_name,food_price,food_description,food_img,userEmail,hotel_id,category_name):
        self.food_id = str(uuid_from_string(food_id))
        self.food_name = food_name
        self.food_price = food_price
        self.food_description = food_description
        self.food_img = food_img
        self.userEmail = userEmail
        self.hotel_id = hotel_id
        self.category_name = category_name
    
    