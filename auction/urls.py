from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns =[
    path('newproduct/',add_product,name='newproduct'),
    path ('auction_by_category/<str:category_id>' ,auction_by_category,name='auction_by_category'),
    path('register/',register,name='Register'),
    path('login/',Login,name='Login'),
    path('logout/', logout_view, name='logout'),
    path('auction/details/<str:auction>/', auction_details, name='auction_details'),
    path('auction_search/', auction_search, name='auction_search'),
    path('Auction/<str:auction_id>',auction_page,name='auction'),
    path('auctions/history',auctions_history,name='auctions_history'),
    
    
    path('auction/customers', auctions_by_customer, name='auctions_by_customers'),

    path('', Home, name='Home'),
    path('<str:category>/', Home, name='Home'),


]