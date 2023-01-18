from django.urls import path
from . import views

urlpatterns = [
    path('all_product/', views.all_product),
    path('address/', views.address),
    path('add_order/', views.add_orders),
    path('history_order/', views.history_order),
]