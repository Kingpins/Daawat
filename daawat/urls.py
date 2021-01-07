from django.contrib import admin
from django.urls import path
from .views.home import Index 
from .views.signup import Signup
from .views.login import Login , logout
from .views.hotel import Hotel, generate_qr, print_qr
from .views.food import Food, update_food, delete_food
from .views.category import Category
from .views.menu import Menu, add_customer, loading, main_menu, main_items
from .views.cart import Cart
from .views.placeorder import PlaceOrder, create_invoice
from .views.makebill import MakeBill
from .views.allorders import AllOrders, decline, order_status, bill_paid
from .middlewares.auth import  auth_middleware


urlpatterns = [
    # This is the home page
    path('', Index.as_view(), name='homepage'),
    
    # The Hotel page where in user creates menu by adding food and categories,
    # the qr-generation for respective table no,
    # monitoring all the orders and checking the status of customers,
    # all these functionalities are handled by the following Views.py files.
    path('hotel', auth_middleware(Hotel.as_view()) , name='hotel'),
    path('food', auth_middleware(Food.as_view()) , name='food'),
    path('category', auth_middleware(Category.as_view()) , name='category'),
    path('update_food', auth_middleware(update_food) , name='update_food'),
    path('delete_food', auth_middleware(delete_food) , name='delete_food'),
    path('generate_qr', auth_middleware(generate_qr) , name='generate_qr'),
    path('print_qr', auth_middleware(print_qr) , name='print_qr'),
    path('allorders', auth_middleware(AllOrders.as_view()) , name='allorders'),
    path('order_status', auth_middleware(order_status) , name='order_status'),
    path('decline', auth_middleware(decline) , name='decline'),
    path('bill_paid', auth_middleware(bill_paid) , name='bill_paid'),

    # The Menu displaying to customers, adding items to cart and finally printing out bill
    # functionalities are handled by the following Views.py files.
    path('<str:hotel_id>/<str:table_no>',Menu.as_view(),name="home_menu"),
    path('add_customer', add_customer , name='add_customer'),
    path('loading', loading , name='loading'),
    path('main_menu', main_menu , name='main_menu'),
    path('main_items', main_items , name='main_items'),
    path('placeorder',PlaceOrder.as_view(),name="placeorder"),
    path('makebill',MakeBill.as_view(),name="makebill"),
    path('cart',Cart.as_view(),name='cart'),
    path('create_invoice',create_invoice,name='create_invoice'),
    
    # The login and Sign-up functionalities are handled by the following Views.py files.
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    

]
