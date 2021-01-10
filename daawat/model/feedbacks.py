from daawat.util.data_type_util import uuid_from_string, format_timestamp
from datetime import datetime

# Feedbacks model, for feedbacks table
class Feedbacks(object):
    def __init__(self, customer_id, hotel_id, customer_name,time_of_feedback,ratings,feedback_comment):
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.customer_name = customer_name
        self.ratings = str(ratings)
        self.feedback_comment = feedback_comment
        self.time_of_feedback =datetime.timestamp(time_of_feedback)
    
    