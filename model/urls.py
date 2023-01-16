from django.urls import path
from . import views

urlpatterns = [
    path('all_product/', views.all_product),
    path('address/', views.address),
    # path('add_produk/', views.addProduk),
    # path('auth/', views.auth),
]