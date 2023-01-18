from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *


# Register your models here.
admin.site.unregister(Group)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('nama_lengkap', 'no_hp', 'alamat')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
                                    'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('id_pengguna', 'username', 'no_hp', 'alamat')


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("product_type_id", "name")


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("product_id", "name", "price", "stock", "product_type")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "created_at", "updated_at",
                    "gross_amount", "status")


@admin.register(OrderDetails)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_detail_id", "order", "product", "qty")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "product", "user", "stock")
