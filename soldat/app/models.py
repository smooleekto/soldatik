from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.



class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    price = models.FloatField()
    name = models.CharField(max_length=20, help_text='Enter product name')
    quantity = models.IntegerField(default=1)
    description = models.TextField(max_length=150)
    photo = models.ImageField(upload_to='products_images')
    vendor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return (self.name)

    @property
    def vendor_name(self):
        return self.vendor_id.username

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    mark = models.IntegerField()
    comment = models.TextField(max_length=140)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    def __str__(self):
        return (self.comment)

class Replies(models.Model):
    reply_id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE)
    comment = models.TextField(max_length=140)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return (self.mark, self.comment)
    
    @property
    def product_id(self):
        return self.comment_id.product_id

    @property
    def username(self):
        return self.user_id.username


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    post_office = models.CharField(max_length=40)
    customer_first_name = models.CharField(max_length=40, default='Anonymous')
    customer_last_name = models.CharField(max_length=40, default='Anonymous')
    customer_phone = models.CharField(max_length=40, default='Anonymous')
    time = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_customer')
    vendor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_vendor')
    status = models.CharField(max_length=40, default='Waiting for sending')
    def __str__(self):
        return (self.order_id, self.post_office, self.time)

    @property
    def vendor_name(self):
        return self.vendor_id.username
    
    @property
    def customer_name(self):
        return self.customer_id.username


class ProductsOrders(models.Model):
    product_order_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=1)

    @property
    def product_name(self):
        return self.product_id.name

    @property
    def photo(self):
        return self.product_id.photo


class ProductsBid(models.Model):
    product_bid_id = models.AutoField(primary_key=True)
    new_price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default='Waiting')
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid_vendor')
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    
    
    @property
    def customer_name(self):
        return self.customer_id.username

    @property
    def vendor_name(self):
        return self.vendor_id.username

    @property
    def product_name(self):
        return self.product_id.name


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

