from daawat.util.data_type_util import uuid_from_string, format_timestamp

# Hotels model, for hotels table
class Hotels(object):
    def __init__(self, hotel_id, hotel_name,hotel_bio,hotel_address,hotel_phone,hotel_tables,hotel_logo,userEmail):
        self.hotel_id = str(uuid_from_string(hotel_id))
        self.hotel_name = hotel_name
        self.hotel_bio = hotel_bio
        self.hotel_address = hotel_address
        self.hotel_phone = hotel_phone
        self.hotel_tables = hotel_tables
        self.hotel_logo = hotel_logo
        self.userEmail = userEmail
    
    