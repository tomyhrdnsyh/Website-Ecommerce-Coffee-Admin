from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


# Create your views here.
@api_view(['GET'])
def all_product(request):
    product = Products.objects.values('product_id', 'name', 'price', 'stock', 'product_type__name')
    return Response(product)


@api_view(['GET'])
def address(request):
    alamat_user = CustomUser.objects.values('id_pengguna', 'nama_lengkap', 'no_hp', 'alamat')
    return Response(alamat_user)


@api_view(['POST'])
def addOrders(request):
    data = request.data
    """
       sample_body = {
           "nama_produk": "Jordan 1 Kg",
           "jenis_produk": "herbisida",
           "no_faktur_pembelian": "42",
           "kuantitas": "9",
           "harga_satuan": "20000.0",
           "tanggal_kadaluarsa": "24 Nov 2022"
       }
       """
    # add_produk = Order(
    #     product
    # )
