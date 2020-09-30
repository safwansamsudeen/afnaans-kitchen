from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from random import randint


def random_id():
    n = 12
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=100)
    confirm_id = models.BigIntegerField(default=random_id)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class FoodTypeModel(models.Model):
    short_name = models.CharField(max_length=50)
    long_name = models.CharField(max_length=50)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.long_name


class FoodItemModel(models.Model):
    name = models.CharField(max_length=200)
    food_item_type = models.ForeignKey(
        FoodTypeModel, on_delete=models.DO_NOTHING)
    price = models.IntegerField()
    main_image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField()
    veg = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class TeamModel(models.Model):
    name = models.CharField(max_length=200)
    positions = models.TextField()
    main_image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField()
    email_address = models.EmailField(max_length=254)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
