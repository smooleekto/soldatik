# Generated by Django 4.1.3 on 2022-11-19 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('mark', models.IntegerField()),
                ('comment', models.TextField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.IntegerField(primary_key=True, serialize=False)),
                ('post_office', models.CharField(max_length=40)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('name', models.CharField(help_text='Enter product name', max_length=20)),
                ('description', models.TextField(max_length=150)),
                ('photo', models.ImageField(upload_to='img/', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(help_text='Enter username', max_length=20)),
                ('password', models.CharField(max_length=16)),
                ('user_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Replies',
            fields=[
                ('reply_id', models.IntegerField(primary_key=True, serialize=False)),
                ('comment', models.TextField(max_length=140)),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.comments')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.users')),
            ],
        ),
        migrations.CreateModel(
            name='ProductsOrders',
            fields=[
                ('product_order_id', models.IntegerField(primary_key=True, serialize=False)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.orders')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.products')),
            ],
        ),
        migrations.CreateModel(
            name='ProductsBid',
            fields=[
                ('product_bid_id', models.IntegerField(primary_key=True, serialize=False)),
                ('new_price', models.IntegerField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.users')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.products')),
                ('vendor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_vendor', to='app.users')),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='vendor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.users'),
        ),
        migrations.AddField(
            model_name='orders',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_customer', to='app.users'),
        ),
        migrations.AddField(
            model_name='orders',
            name='vendor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_vendor', to='app.users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.products'),
        ),
    ]
