# Generated by Django 4.1.3 on 2022-11-22 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_comments_customer_id_alter_orders_customer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='photo',
            field=models.ImageField(default='default.jpg', upload_to='products_images'),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
