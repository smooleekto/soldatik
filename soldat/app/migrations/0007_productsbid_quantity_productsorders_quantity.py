# Generated by Django 4.1.3 on 2022-12-23 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_products_quantity_productsbid_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsbid',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='productsorders',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]