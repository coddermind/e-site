from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    category=models.CharField(max_length=100,default="All")
    date_added=models.DateTimeField(auto_now_add=True)
    description=models.TextField()

    image_1=models.ImageField(upload_to="images/")
    image_2=models.ImageField(upload_to="images/",null=True,blank=True)
    image_3=models.ImageField(upload_to="images/",null=True,blank=True)
    image_4=models.ImageField(upload_to="images/",null=True,blank=True)
    image_5=models.ImageField(upload_to="images/",null=True,blank=True)
    image_6=models.ImageField(upload_to="images/",null=True,blank=True)
    image_7=models.ImageField(upload_to="images/",null=True,blank=True)
    image_8=models.ImageField(upload_to="images/",null=True,blank=True)

    video_1=models.FileField(upload_to="videos/",null=True,blank=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.TextField(null=True)
    product_name=models.TextField(null=True)
    product_price=models.TextField(null=True)
    product_quantity=models.TextField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_placed = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.order_placed}"
    


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(default=timezone.now)  # Add timestamp field