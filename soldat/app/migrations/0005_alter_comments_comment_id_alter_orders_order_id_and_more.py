# Generated by Django 4.1.3 on 2022-11-25 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_products_photo_alter_products_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='products',
            name='photo',
            field=models.ImageField(upload_to='products_images'),
        ),
        migrations.AlterField(
            model_name='productsbid',
            name='product_bid_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='productsorders',
            name='product_order_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='replies',
            name='reply_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]