# Generated by Django 4.1.3 on 2022-12-24 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_orders_customer_first_name_orders_customer_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsorders',
            name='price',
            field=models.FloatField(default=1),
        ),
    ]
