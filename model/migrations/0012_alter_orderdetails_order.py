# Generated by Django 4.1.5 on 2023-01-25 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0011_remove_products_payment_type_order_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(db_column='id_order', on_delete=django.db.models.deletion.CASCADE, to='model.order'),
        ),
    ]
