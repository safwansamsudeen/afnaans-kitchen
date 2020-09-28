from django.shortcuts import render, redirect
from django.contrib import messages, auth

from .models import FoodItemModel, TeamModel, FoodTypeModel, CustomUser


def index(req):
    return render(req, 'index.html')


def about(req):
    people = TeamModel.objects.all()
    return render(req, 'about.html', {
        'people': people
    })


def menu(req):
    items = FoodItemModel.objects.all().filter(is_available=True)
    types = FoodTypeModel.objects.all()
    local_types_long = [_type.long_name for _type in types]
    local_types = [_type.id for _type in types]
    local_items = [items.filter(food_item_type=_type) for _type in local_types]
    return render(req, 'menu.html', {
        'types': local_types_long,
        'items': local_items,
    })


def login(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(req, user)
            messages.success(req, "You are logged in.")
            return redirect("login")
        else:
            messages.error(req, "Invalid credentials")
            return redirect("login")
    else:
        return render(req, 'login.html')


def register(req):
    if req.method == "POST":
        phone_number = req.POST["phone_number"]
        address = req.POST["address"]
        username = req.POST["username"]
        email = req.POST["email"]
        password = req.POST["password"]
        password2 = req.POST["password2"]

        # Password matches validation
        if password != password2:
            messages.error(req, "Passwords do not match!")
            return redirect("register")

        # Username unique validation
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(req, "Username already exists!")
            return redirect("register")

        # Email unique validation
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(req, "Email already exists!")
            return redirect("register")

        else:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, phone_number=phone_number, address=address)
            messages.success(req, "You are registered and can login.")
            return redirect("login")
    else:
        return render(req, "register.html")
