from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


# Create your views here.
@api_view(['GET'])
def all_product(request):
    product = Products.objects.values('product_id', 'name', 'price', 'stock', 'product_type__name')
    for item in product:
        item['price'] = f"Rp. {item['price']:,}"

    return Response(product)


@api_view(['GET'])
def address(request):
    alamat_user = CustomUser.objects.values('id_pengguna', 'nama_lengkap', 'no_hp', 'alamat')
    return Response(alamat_user)


@api_view(['POST'])
def history_order(request):
    """
       sample_body = {
           "username": "admin-aja"
       }
       """
    data = request.data
    try:
        user = CustomUser.objects.get(username=data.get("username"))
    except CustomUser.DoesNotExist:
        response = {"message": "User tidak ditemukan"}
    else:
        response = OrderDetails.objects.filter(order__user=user).values('qty',
                                                                        'product__name',
                                                                        'order__gross_amount',
                                                                        'order__status')
        for item in response:
            item['order__gross_amount'] = f"Rp. {item['order__gross_amount']:,}"

    return Response(response)


@api_view(['POST'])
def add_orders(request):
    data = request.data
    """
       sample_body = {
           "product_id": "1",
           "username": "admin-aja",
           "quantity": "42"
       }
       """

    product = Products.objects.get(product_id=data.get('product_id'))
    add_order = Order(
        user=CustomUser.objects.get(username=data.get("username")),
        gross_amount=product.price * int(data.get('quantity')),
        status='Belum diterima'
    )
    add_order_detail = OrderDetails(
        order=add_order,
        product=product,
        qty=data.get('quantity')
    )
    add_order.save()
    add_order_detail.save()

    return Response(data)
