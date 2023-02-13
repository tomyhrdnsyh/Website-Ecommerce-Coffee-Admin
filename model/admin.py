from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
import csv
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

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


class OrderDetailInline(admin.TabularInline):
    model = OrderDetails
    extra = 1


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        # field_names.append('user__address')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            print([getattr(obj, field) for field in field_names])
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportCsvMixin):
    inlines = [OrderDetailInline]
    list_display = ("order_id", "transaction_time", "user", "get_products",
                    "payment_type", "payment_status", "total", "status")

    search_fields = ['order_id', 'transaction_time', 'user__username', 'gross_amount', 'status',
                     'payment_type', 'payment_status']

    @admin.display(ordering='product__price', description='Total')
    def total(self, obj):
        total = sum([item['price'] * item['orderdetails__qty'] for item in obj.product.values('price',
                                                                                              'orderdetails__qty')])
        return total

    @admin.display(ordering='product__name', description='Product')
    def get_products(self, obj):
        return " || ".join([f"{p['orderdetails__qty']}x {p['name']}" for p in obj.product.values('name',
                                                                                                 'orderdetails__qty')])

    actions = ['export_pdf']

    def export_pdf(self, request, queryset):
        context = {}
        order = []
        for item in queryset:
            order.append(
                {
                    'order_id': item.order_id,
                    'transaction_time': item.transaction_time,
                    'user': item.user,
                    'product_name': " || ".join([f"{p['orderdetails__qty']}x {p['name']}" for p in item.product.values('name', 'orderdetails__qty')]),
                    'payment_type': item.payment_type if item.payment_type is not None else '-',
                    'payment_status': item.payment_status if item.payment_status is not None else '-',
                    'total': sum([total['price'] * total['orderdetails__qty'] for total in item.product.values('price', 'orderdetails__qty')]),
                    'status': item.status
                }
            )

        context['order'] = order
        load_template = 'pdf-order.html'
        context['segment'] = load_template
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    export_pdf.short_description = "Cetak PDF Order yang dipilih"


# @admin.register(OrderDetails)
# class OrderAdminDetails(admin.ModelAdmin):
#     list_display = ("order", "get_user", "product", "qty", "get_created_at", "get_payment_type",
#                     "get_gross_amount", "get_status")
#
#     @admin.display(ordering=['order__user'], description='User')
#     def get_user(self, obj):
#         return obj.order.user
#
#     @admin.display(ordering=['order__created_at'], description='Transaction time')
#     def get_created_at(self, obj):
#         return obj.order.created_at
#
#     @admin.display(ordering=['order__payment_type'], description='Payment type')
#     def get_payment_type(self, obj):
#         return obj.order.payment_type
#
#     @admin.display(ordering=['product__price'], description='Total')
#     def get_gross_amount(self, obj):
#         return obj.product.price * obj.qty
#
#     @admin.display(ordering=['order__status'], description='Status')
#     def get_status(self, obj):
#         return obj.order.status


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "product", "user", "qty")
