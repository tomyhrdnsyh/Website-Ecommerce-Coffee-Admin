from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import pandas as pd
from collections import defaultdict


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
        order = Order.objects.order_by('-order_id').filter(user=user). \
            values('order_id', 'product__name', 'gross_amount', 'status',
                   'product__orderdetails__qty')

        df = pd.DataFrame(order)
        df_group = df.groupby('order_id').sum().to_dict(orient='index')

        dd = defaultdict(list)
        for item in order:
            dd[item['order_id']].append(
                item['product__name']
            )
        print(dd)
    return Response(order)


@api_view(['POST'])
def history_order_details(request):
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
        response = OrderDetails.objects.order_by('-order_detail_id').filter(order__user=user).values('qty',
                                                                                                     'product__name',
                                                                                                     'order__gross_amount',
                                                                                                     'order__status')
        for item in response:
            item['order__gross_amount'] = f"Rp. {item['order__gross_amount']:,}"

    return Response(response)


@api_view(['POST'])
def add_orders(request):
    """
       sample_body = {
           "product_id": "1",
           "username": "admin-aja",
           "quantity": "42"
       }
       """
    data = request.data
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


@api_view(['POST'])
def add_order_from_cart(request):
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
        cart = Cart.objects.filter(user=user)

        add_order = Order(
            user=user,
            gross_amount=sum(item.qty * item.product.price for item in cart),
            status='Belum diterima'
        )
        add_order.save()

        for item in cart:
            add_order_detail = OrderDetails(
                order=add_order,
                product=item.product,
                qty=item.qty
            )
            add_order_detail.save()

        cart.delete()
        response = {"message": "Checkout berhasil!"}

    return Response(response)


@api_view(['POST'])
def get_cart(request):
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
        response = Cart.objects.filter(user=user).values(
            'cart_id', 'product__name',
            'product__price', 'product__stock',
            'product__product_type__name',
            'qty'
        )
    return Response(response)


@api_view(['POST'])
def add_cart(request):
    """
       sample_body = {
           "product_id": "1",
           "username": "admin-aja",
           "stock": "1"
       }
       """
    data = request.data
    try:
        user = CustomUser.objects.get(username=data.get("username"))
    except CustomUser.DoesNotExist:
        responses = {"message": "User tidak ditemukan"}
    else:
        product = Products.objects.get(product_id=data.get('product_id'))

        obj, created = Cart.objects.update_or_create(
            product=product,
            user=user,
            defaults={'qty': data.get('stock')}
        )
        responses = {"message": f"{product.name} added to cart!"}
    return Response(responses)


@api_view(['POST'])
def delete_cart(request):
    """
       sample_body = {"cart_id": "1"}
       """
    data = request.data

    try:
        del_cart = Cart.objects.get(cart_id=data.get('cart_id'))
    except Cart.DoesNotExist:
        response = {"message": "Produk tidak ditemukan!"}
    else:

        del_cart.delete()
        response = {"message": f"{del_cart.product} Deleted!"}

    return Response(response)
