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


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("product_category_id", "name")


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("product_id", "name", "price", "stock", "product_type", "product_category")


class TestingAdmin(admin.TabularInline):
    model = OrderDetails
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [TestingAdmin]
    list_display = ("order_id", "user", "created_at", "gross_amount", "status")
    readonly_fields = ("order_id", "user")
    # search_fields = ['user']


@admin.register(OrderDetails)
class OrderAdminDetails(admin.ModelAdmin):
    list_display = ("order", "get_user", "product", "qty", "get_created_at", "get_payment_type",
                    "get_gross_amount", "get_status")

    @admin.display(ordering=['order__user'], description='User')
    def get_user(self, obj):
        return obj.order.user

    @admin.display(ordering=['order__created_at'], description='Transaction time')
    def get_created_at(self, obj):
        return obj.order.created_at

    @admin.display(ordering=['order__payment_type'], description='Payment type')
    def get_payment_type(self, obj):
        return obj.order.payment_type

    @admin.display(ordering=['product__price'], description='Total')
    def get_gross_amount(self, obj):
        return obj.product.price * obj.qty

    @admin.display(ordering=['order__status'], description='Status')
    def get_status(self, obj):
        return obj.order.status


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "product", "user", "qty")
