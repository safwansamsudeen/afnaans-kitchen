from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import FoodItemModel, TeamModel, FoodTypeModel, CustomUser


def confirm_account(req, account_id):
    if CustomUser.objects.all().filter(confirm_id=account_id, confirmed=False):
        user = CustomUser.objects.get(confirm_id=account_id)
        user.confirmed = True
        user.save()
        return redirect('login')


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
        print(user)
        if user and CustomUser.objects.all().filter(user=user, confirmed=True):
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
        elif User.objects.filter(username=username).exists():
            messages.error(req, "Username already exists!")
            return redirect("register")

        # # Email unique validation
        # elif User.objects.filter(email=email).exists():
        #     messages.error(req, "Email already exists!")
        #     return redirect("register")

        else:
            try:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                custom_user = CustomUser.objects.create(
                    user=user, phone_number=phone_number, address=address)
                send_mail("Afnaan's Kitchen Account confirmation",
                          f"Thanks for signing up to Afnaan's Kitchen! We hope you will have an excellent time eating our yummy pizzas! Just one last step...\n\nHead over to {req.META['HTTP_HOST']}/confirm_account/{custom_user.confirm_id}",
                          'safwansamsudeen@gmail.com',
                          [email, 'safwansamsudeen@gmail.com'],
                          fail_silently=False
                          )
                messages.success(
                    req, "We sent you a confirmation link. Please check your inbox.")
                return redirect("login")
            except Exception as e:
                print(e)
                messages.error(
                    req, "There was an error. Please try again.")
                return redirect("register")
    else:
        return render(req, "register.html")
