from daawat.dao.session_manager import SessionManager
from daawat.dao.users_dao import UsersDAO
from daawat.dao.hotels_dao import HotelsDAO
from daawat.dao.foods_dao import FoodsDAO
from daawat.dao.categorys_dao import CategorysDAO
from daawat.dao.customer_dao import CustomersDAO
from daawat.dao.generate_qr_dao import GenerateQRsDAO
from daawat.dao.orders_dao import OrdersDAO
from daawat.dao.invoices_dao import InvoicesDAO
from daawat.dao.feedbacks_dao import FeedbacksDAO

class AstraService(object):

    # Necessary variable declarations
    user_dao = None
    hotel_dao = None
    food_dao = None
    category_dao = None
    customer_dao = None
    generate_qr_dao = None
    order_dao = None
    invoice_dao = None
    feedback_dao = None
    _session_manager = SessionManager()
    _session = None

    def __init__(self):
        pass

    def get_session(self):
        if self._session is None:
            self._session = self._session_manager.get_instance().connect()

        return self._session

    # connecting to ASTRA DATASTAX DB
    def connect(self):
        return self._session_manager.connect()

    # checking DB connection
    def check_connection(self):
        return self._session_manager.check_connection()

    # The following functions are used to provide _session for all the Data Access Objects,
    # As listed UserDAO, HotelDAO, FoodDAO, CategoryDAO, CustomerDAO, OrderDAO, InvoiceDAO, FeedbackKDAO
    def get_user_dao(self):
        if self.user_dao is None:
            self.user_dao = UsersDAO(self.get_session())

        return self.user_dao

    def get_hotel_dao(self):
        if self.hotel_dao is None:
            self.hotel_dao = HotelsDAO(self.get_session())

        return self.hotel_dao

    def get_food_dao(self):
        if self.food_dao is None:
            self.food_dao = FoodsDAO(self.get_session())

        return self.food_dao

    def get_category_dao(self):
        if self.category_dao is None:
            self.category_dao = CategorysDAO(self.get_session())

        return self.category_dao

    def get_customer_dao(self):
        if self.customer_dao is None:
            self.customer_dao = CustomersDAO(self.get_session())

        return self.customer_dao

    def get_generate_qr_dao(self):
        if self.generate_qr_dao is None:
            self.generate_qr_dao = GenerateQRsDAO(self.get_session())

        return self.generate_qr_dao

    def get_order_dao(self):
        if self.order_dao is None:
            self.order_dao = OrdersDAO(self.get_session())

        return self.order_dao

    def get_invoice_dao(self):
        if self.invoice_dao is None:
            self.invoice_dao = InvoicesDAO(self.get_session())

        return self.invoice_dao

    def get_feedback_dao(self):
        if self.feedback_dao is None:
            self.feedback_dao = FeedbacksDAO(self.get_session())

        return self.feedback_dao

    # functions used to service login and signup functionalities
    def create_new_user(self, first_name, last_name, phone, email, password):
        return self.get_user_dao().create_user(first_name, last_name, phone, email, password)

    def get_user_exits(self,email):
        return self.get_user_dao().get_user_exits(email)

    def get_user_by_email(self,email):
        return self.get_user_dao().get_user_by_email(email)

    # functions used to add hotel and check whether hotel exists by email_id or hotel_id
    def create_new_hotel(self, hotel):
        return self.get_hotel_dao().create_hotel(hotel)

    def get_hotel_by_email(self,email):
        return self.get_hotel_dao().get_hotel_by_email(email)

    def get_hotel_exits(self,email):
        return self.get_hotel_dao().get_hotel_exits(email)

    def get_hotel_by_hotel_id(self,hotel_id):
        return self.get_hotel_dao().get_hotel_by_hotel_id(hotel_id)

    def get_hotel_exits_by_hotel_id(self,hotel_id):
        return self.get_hotel_dao().get_hotel_exits_by_hotel_id(hotel_id)

    # functions used to add category and check whether category exists by email_id or hotel_id or category_name
    def create_new_category(self, category):
        return self.get_category_dao().create_category(category)
    
    def get_category_exits(self,email):
        return self.get_category_dao().get_categroy_exits(email)

    def get_category_by_email(self,email):
        return self.get_category_dao().get_category_by_email(email)

    def get_category_by_hotel_id(self,hotel_id):
        return self.get_category_dao().get_category_by_hotel_id(hotel_id)

    def get_category_id_by_category_name(self,category_name):
        return self.get_category_dao().get_category_id_by_category_name(category_name)

    # functions used to add, delete and update food and retrive food by email_id or food_id
    def create_new_food(self, food):
        return self.get_food_dao().create_food(food)

    def update_food(self, food, food_id):
        return self.get_food_dao().update_food(food,food_id)
    
    def delete_food(self, food_id):
        return self.get_food_dao().delete_food(food_id)

    def delete_food(self, food_id):
        return self.get_food_dao().delete_food(food_id)
    
    def get_food_by_email(self,email):
        return self.get_food_dao().get_food_by_email(email)

    def get_food_by_food_id(self,food_id):
        return self.get_food_dao().get_food_by_food_id(food_id)

    def get_food_by_food_ids(self,food_ids):
        return self.get_food_dao().get_food_by_food_ids(food_ids)

    def get_food_by_category_name(self,category_name):
        return self.get_food_dao().get_food_by_category_name(category_name)
    
    # functions used to add, update, delete and change status of customers and get customers by customer_id or hotel_id
    def create_new_customer(self, customer):
        return self.get_customer_dao().create_customer(customer)

    def customer_status_by_customer_id(self, customer_id):
        return self.get_customer_dao().get_customer_status_by_customer_id(customer_id)
    
    def get_customer_by_hotel_id(self, hotel_id):
        return self.get_customer_dao().get_customer_by_hotel_id(hotel_id)

    def get_customer_by_customer_id(self, customer_id):
        return self.get_customer_dao().get_customer_by_customer_id(customer_id)

    def update_customer_by_customer_id(self, customer_id):
        return self.get_customer_dao().update_customer(customer_id)

    def delete_customer(self, customer_id):
        return self.get_customer_dao().delete_customer(customer_id)

    # functions used to create generate_qr and gets qr_images by email_id    
    def create_generate_qr(self, generateqr):
        return self.get_generate_qr_dao().create_generate_qr(generateqr)
    
    def get_generate_qr_exits(self,email):
        return self.get_generate_qr_dao().get_generate_by_email(email)

    # functions used to create orders and gets orders
    def create_order(self, order):
        return self.get_order_dao().create_order(order)

    def get_order(self, hotel_id,customer_id):
        return self.get_order_dao().get_orders(hotel_id,customer_id)

    def update_order_status(self, hotel_id,customer_id,order_id,time_of_order):
        return self.get_order_dao().update_order_status(hotel_id,customer_id,order_id,time_of_order)

    # functions used create invoices and get invoices
    def create_invoice(self, invoice):
        return self.get_invoice_dao().create_invoice(invoice)

    def get_invoice_by_invoice_id(self, invoice_id):
        return self.get_invoice_dao().get_invoice_by_invoice_id(invoice_id)

    def get_invoice_by_invoice_id_with_limit_1(self, invoice_id):
        return self.get_invoice_dao().get_invoice_by_invoice_id_with_limit(invoice_id)

    def get_invoice_by_hotel_id(self, hotel_id):
        return self.get_invoice_dao().get_invoice_by_hotel_id(hotel_id)

    def get_invoice_by_customer_id(self, customer_id):
        return self.get_invoice_dao().get_invoice_by_customer_id(customer_id)

    # functions used create feedback and get feeddbacks by hotel_id
    def create_feedback(self, feedback):
        return self.get_feedback_dao().create_feedback(feedback)

    def get_feedbacks_by_hotel_id(self, hotel_id):
        return self.get_feedback_dao().get_feedback_by_hotel_id(hotel_id)

    def get_feedbacks_exists(self, hotel_id):
        return self.get_feedback_dao().get_feedback_exits(hotel_id)


astra_service = AstraService()
