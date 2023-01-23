from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth),
    path('all_product/', views.all_product),
    path('address/', views.address),
    path('registration/', views.registration),
    path('edit_user_profile/', views.edit_user_profile),
    path('add_order/', views.add_orders),
    path('add_order_from_cart/', views.add_order_from_cart),
    path('history_order/', views.history_order),
    path('history_order_detail/', views.history_order_details),
    path('acc_order/', views.acc_order),
    path('add_cart/', views.add_cart),
    path('get_cart/', views.get_cart),
    path('delete_cart/', views.delete_cart),
]