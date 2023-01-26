from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import pandas as pd
from collections import defaultdict
from datetime import datetime


# Create your views here.
@api_view(['GET'])
def all_product(request):
    product = Products.objects.values('product_id', 'name', 'price', 'stock', 'product_type__name',
                                      'product_category__name')
    for item in product:
        item['price'] = f"Rp. {item['price']:,}"

    return Response(product)


@api_view(['POST'])
def auth(request):
    data = request.data

    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        response = {'message': '200'}
    else:
        response = {'message': '400'}
    return Response(response)


@api_view(['POST'])
def registration(request):
    """
       sample_body = {
           "username": "admin1",
           "full_name": "Admin",
           "no_hp": "08228789909",
           "email": "admin1@gmail.com",
           "password": "rahasia2022",
           "address": "Jakarta Indonesia"
       }
       """
    data = request.data
    user = CustomUser(
        username=data.get('username'),
        nama_lengkap=data.get('full_name'),
        email=data.get('email'),
        no_hp=data.get('no_hp'),
        alamat=data.get('address')
    )
    user.set_password(data.get('password'))
    user.save()

    print(user)

    response = {"message": "Create user done!"}
    return Response(response)


@api_view(['POST'])
def address(request):
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
        response = {
            'id_pengguna': user.id_pengguna,
            'nama_lengkap': user.nama_lengkap,
            'no_hp': user.no_hp,
            'alamat': user.alamat,
            'email': user.email,
        }
    return Response(response)


@api_view(['POST'])
def edit_user_profile(request):
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
        if data.get('nama_lengkap'):
            user.nama_lengkap = data.get('nama_lengkap')
        if data.get("no_hp"):
            user.no_hp = data.get("no_hp")
        if data.get("email"):
            user.email = data.get("email")
        if data.get("password"):
            user.set_password(data.get("password"))
        if data.get("alamat"):
            user.alamat = data.get("alamat")
        user.save()
        response = {"message": "Edit profile berhasil!"}

    return Response(response)


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
                   'orderdetails__qty')

        df = pd.DataFrame(order)
        df_group = df.groupby(['order_id', 'product__name', 'status']).sum().to_dict(orient='index')

        raw_dd = defaultdict(list)
        for index, row in df_group.items():
            raw_dd[index[0]].append(
                {
                    'qty': int(row['orderdetails__qty']),
                    'product__name': index[1],
                    'order__gross_amount': f"{row['gross_amount']:,}",
                    'order__status': index[2]
                }
            )

        response = []
        for key, value in raw_dd.items():
            name = '+'.join([item.get('product__name') for item in value])
            price = '+'.join([item.get('order__gross_amount') for item in value])
            qty = '+'.join([str(item.get('qty')) for item in value])

            response.append(
                {
                    'order_id': key,
                    'qty': qty if len(qty) < 4 else qty[:4] + '...',
                    'product__name': name if len(name) < 20 else name[:20] + '...',
                    'order__gross_amount': price if len(price) < 10 else price[:10] + '...',
                    'order__status': value[0].get('order__status')
                }
            )
            response = sorted(response, key=lambda d: d['order_id'], reverse=True)

    return Response(response)


@api_view(['POST'])
def history_order_details(request):
    """
       sample_body = {
           "order_id": "1"
       }
       """
    data = request.data
    try:
        order = Order.objects.filter(order_id=data.get("order_id")).values(
            'order_id', 'orderdetails__qty', 'product__name', 'product__product_type__name', 'product__price'
        )
    except CustomUser.DoesNotExist:
        response = {"message": "Order tidak ditemukan"}
    else:
        response = order

    return Response(response)


@api_view(['POST'])
def acc_order(request):
    """
           sample_body = {
               "order_id": "1"
           }
           """
    data = request.data
    try:
        order = Order.objects.get(order_id=data.get("order_id"))
    except CustomUser.DoesNotExist:
        response = {"message": "Order tidak ditemukan"}
    else:
        order.status = "Diterima"
        order.updated_at = datetime.now()
        order.save()
        response = {"message": f"Pesanan id {order.order_id} diterima"}

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
            'qty', 'product__product_category__name'
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
