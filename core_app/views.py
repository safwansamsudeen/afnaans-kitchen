from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.contrib.auth.hashers import check_password
from .models import FoodItem, PersonInTeam, FoodType, CustomUser, CartItem
from random import randint


def random_id():
    n = 12
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def login_required(func):
    def func_wrapper(req):
        if req.user.is_authenticated and not req.user.is_superuser:
            return func(req, CustomUser.objects.get(user=req.user.id))
        else:
            messages.error(req, "Please login first")
            return redirect('login')
    return func_wrapper


# def cart_details(req):
#     data = []
#     i = 0
#     cart_items = CartItem.objects.filter(
#         user=CustomUser.objects.get(user=req.user.id))
#     for food_item in FoodItem.objects.all():
#         if food_item in [cart_item.item for cart_item in cart_items]:
#             print('In')
#             data.append(cart_items[i].qty)
#             i += 1
#         else:
#             data.append(0)
#     return JsonResponse(data, safe=False)


@login_required
def cart(req, current_user):
    orders = CartItem.objects.filter(user=current_user)
    return render(req, 'cart.html', {
        'cusUser': current_user,
        'orders': orders,
        'total_qty': sum([order.qty for order in orders]),
        'total_price': sum([order.item.price * order.qty for order in orders]),
    })


def change_user_email(req, confirm_id):
    current_user = CustomUser.objects.filter(confirm_id=confirm_id)
    if current_user:
        current_user = current_user[0]
        current_user.user.email = current_user.new_email
        current_user.user.save()
        return redirect('settings')
    else:
        raise Http404('Not found')


@login_required
def change_email(req, current_user):
    if req.method == 'POST':
        try:
            email = req.POST.get("email")

            # Email unique validation
            if User.objects.filter(email=email).exists():
                messages.error(req, "Email is taken!")
                return redirect("register")
            current_user.confirm_id = random_id()
            send_mail(
                "Afnaan's Kitchen Change Email Address",
                f"""Hello,
We have noticed that you have tried to change your account's email address to {email}. Please go to {req.META['HTTP_HOST']}/change_user_email/{current_user.confirm_id} to reconfirm your account. Your account has been temporarily disabled, but you can login as soon as you reconfirm your account.

Best Wishes,
Safwan Samsudeen,
Afnaan's Kitchen
                        """,
                'afnaanskitchen.team@gmail.com',
                [current_user.user.email],
                fail_silently=False
            )
            current_user.new_email = email
            current_user.save()
            messages.success(
                req, 'We have sent you a confirmation email. Please check your old email inbox.')
        except Exception as e:
            print(e)
            messages.error(req,
                           'There was an error while trying to change your email address. Please try again')
    return redirect('settings')


@login_required
def change_password(req, current_user):
    if req.method == 'POST':
        old_password = req.POST.get("old_password")
        new_password = req.POST.get("new_password")
        new_password2 = req.POST.get("new_password2")
        if not check_password(old_password, current_user.user.password):
            messages.error(req, "Incorrect current password!")
            return redirect("settings")
        elif new_password != new_password2:
            messages.error(req, "Passwords do not match!")
            return redirect("settings")
        else:
            current_user.user.set_password(new_password)
            current_user.user.save()
            messages.success(req, "Passwords changed")
            return redirect("login")


@login_required
def logout(req, current_user):
    auth.logout(req)
    messages.success(req, "You are now logged out.")
    return redirect("index")


@login_required
def settings(req, current_user):
    if req.method == 'POST':
        try:
            current_user.phone_number = req.POST.get('phone_number')
            current_user.address = req.POST.get('address')
            current_user.save()
            messages.success(req, 'Your settings have been updated')
        except:
            messages.error(req,
                           'There was an error while trying to save your credentials. Please try again')
    return render(req, 'settings.html', {'curUser': current_user})


def confirm_account(req, account_id):
    if CustomUser.objects.filter(confirm_id=account_id, confirmed=False):
        user = CustomUser.objects.get(confirm_id=account_id)
        user.confirmed = True
        user.save()
        auth.login(req, user)
        return redirect('settings')
    else:
        raise Http404('Not found')


def index(req):
    return render(req, 'index.html')


def about(req):
    people = PersonInTeam.objects.all()
    return render(req, 'about.html', {
        'people': people
    })


def menu(req):
    items = FoodItem.objects.filter(is_available=True)
    types = FoodType.objects.all()
    local_types_long = [_type.long_name for _type in types]
    local_types = [_type.id for _type in types]
    local_items = [items.filter(food_item_type=_type) for _type in local_types]
    data = []
    if req.user.is_authenticated and not req.user.is_superuser:
        i = 0
        cart_items = CartItem.objects.filter(
            user=CustomUser.objects.get(user=req.user.id))
        for food_item in FoodItem.objects.all():
            if food_item in [cart_item.item for cart_item in cart_items]:
                data.append(cart_items[i].qty)
                i += 1
            else:
                data.append(0)
    return render(req, 'menu.html', {
        'types': local_types_long,
        'items': local_items,
        'qtys': data
    })

def login(req):
    if req.method == "POST":
        username=req.POST.get("username")
        password=req.POST.get("password")

        user=auth.authenticate(username=username, password=password)
        print(user)
        if user and CustomUser.objects.filter(user=user, confirmed=True):
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
        phone_number=req.POST.get("phone_number")
        address=req.POST.get("address")
        username=req.POST.get("username")
        email=req.POST.get("email")
        password=req.POST.get("password")
        password2=req.POST.get("password2")
        # Password matches validation
        if password != password2:
            messages.error(req, "Passwords do not match!")
            return redirect("register")

        # Username unique validation
        elif User.objects.filter(username=username).exists():
            messages.error(req, "Username already exists!")
            return redirect("register")

        # Email unique validation
        elif User.objects.filter(email=email).exists():
            messages.error(req, "Email is taken!")
            return redirect("register")

        else:
            try:
                user=User.objects.create_user(
                    username=username, password=password, email=email)
                custom_user=CustomUser.objects.create(
                    user=user, phone_number=phone_number, address=address, confirm_id=random_id())
                send_mail(
                    "Afnaan's Kitchen Account confirmation",
                    f"""Thanks for signing up to Afnaan's Kitchen! We hope you will have an excellent time eating our yummy pizzas! Just one last step...

Head over to {req.META['HTTP_HOST']}/confirm_account/{custom_user.confirm_id} to automatically confirm your account. You will then by redirected to you dashboard. Happy eating!

Best Wishes,
Safwan Samsudeen,
Afnaan's Kitchen
                    """,
                    'afnaanskitchen.team@gmail.com',
                    [email],
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
