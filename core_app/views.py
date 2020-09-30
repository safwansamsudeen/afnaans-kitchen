from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import FoodItemModel, TeamModel, FoodTypeModel, CustomUser, random_id


def login_required(func):
    def func_wrapper(req):
        if req.user.is_authenticated:
            return func(req)
        else:
            messages.error(req, "Please login first")
            return render(req, 'login.html')
    return func_wrapper


@login_required
def change_email(req):
    current_user = CustomUser.objects.get(user=req.user.id)
    if req.method == 'POST':
        try:
            email = req.POST.get("email")
            current_user.confirm_id = random_id()
            # if User.objects.filter(email=email).exists():
            #     messages.error(req, "Email already exists!")
            #     return redirect("settings")
            send_mail(
                "Afnaan's Kitchen Change Email Address",
                f"""Hello,
We have noticed that you have tried to change your account's email address. Please go to {req.META['HTTP_HOST']}/confirm_account/{current_user.confirm_id} to reconfirm your account. Your account has been temporarily disabled, but you can login as soon as you reconfirm your account.
                        
Best Wishes,
Safwan Samsudeen, 
Afnaan's Kitchen
                        """,
                'afnaanskitchen.team@gmail.com',
                [current_user.user.email],
                fail_silently=False
            )
            current_user.user.email = email
            current_user.confirmed = False
            current_user.save()
            current_user.user.save()
            auth.logout(req)
            messages.success(
                req, 'We have sent you a confirmation email. Please check your old email inbox.')
        except Exception as e:
            print(e)
            messages.error(req,
                           'There was an error while trying to change your email address. Please try again')
    return redirect('settings')


@login_required
def change_password(req):
    pass


@login_required
def logout(req):
    auth.logout(req)
    messages.success(req, "You are now logged out.")
    return redirect("index")


@login_required
def settings(req):
    current_user = CustomUser.objects.get(user=req.user.id)
    if req.method == 'POST':
        try:
            current_user.phone_number = req.POST.get('phone_number')
            current_user.address = req.POST.get('address')
            current_user.save()
            messages.success(req, 'Your settings have been updated')
        except:
            messages.error(req,
                           'There was an error while trying to save your credentials. Please try again')
    return render(req, 'settings.html', {'cusUser': current_user})


@login_required
def cart(req):
    pass


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
        username = req.POST.get("username")
        password = req.POST.get("password")

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
        phone_number = req.POST.get("phone_number")
        address = req.POST.get("address")
        username = req.POST.get("username")
        email = req.POST.get("email")
        password = req.POST.get("password")
        password2 = req.POST.get("password2")
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
