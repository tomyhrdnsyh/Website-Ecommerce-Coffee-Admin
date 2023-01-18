from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    first_name = None
    last_name = None

    id_pengguna = models.AutoField(primary_key=True)
    nama_lengkap = models.CharField(max_length=100, null=True)
    no_hp = models.CharField(max_length=20, null=True)
    alamat = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name = 'pengguna'
        verbose_name_plural = 'pengguna'
        db_table = 'pengguna'


class ProductType(models.Model):
    product_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}-{self.product_type}"

    class Meta:
        verbose_name_plural = 'Products'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ManyToManyField(Products, through='OrderDetails')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    gross_amount = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.order_id)


class OrderDetails(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name_plural = 'Order details'


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return f"{user}-{product}"
