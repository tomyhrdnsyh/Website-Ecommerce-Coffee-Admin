# Generated by Django 4.1.5 on 2023-01-17 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0004_rename_product_type_producttype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.IntegerField(),
        ),
    ]
