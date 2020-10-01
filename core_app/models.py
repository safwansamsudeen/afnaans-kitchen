from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    new_email = models.CharField(max_length=200, default='')
    phone_number = models.CharField(max_length=100)
    confirm_id = models.BigIntegerField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class FoodType(models.Model):
    short_name = models.CharField(max_length=50)
    long_name = models.CharField(max_length=50)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.long_name


class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    food_item_type = models.ForeignKey(
        FoodType, on_delete=models.CASCADE)
    price = models.IntegerField()
    main_image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField()
    veg = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class PersonInTeam(models.Model):
    name = models.CharField(max_length=200)
    positions = models.TextField()
    main_image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField()
    email_address = models.EmailField(max_length=254)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=datetime.now)
