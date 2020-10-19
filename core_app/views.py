from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from .models import FoodItem, PersonInTeam, FoodType, CustomUser, CartItem, Order
from random import randint
import json
import core_app


# Helper functions
def login_required(func):
    def func_wrapper(req):
        if is_logged_in(req):
            return func(req, CustomUser.objects.get(user=req.user.id))
        else:
            messages.error(req, "Please login first")
            return redirect('login')
    return func_wrapper


def is_logged_in(req):
    return req.user.is_authenticated and not req.user.is_staff


def random_id(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# Controllers


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
    qtys = {str(item): CartItem.objects.filter(
        item=item) or 0 for item in items}
    for item in items:
        try:
            qtys[str(item)] = CartItem.objects.get(item=item).qty
        except core_app.models.CartItem.DoesNotExist:
            qtys[str(item)] = 0
    return render(req, 'menu.html', {
        'types': local_types_long,
        'items': local_items,
        'qtys': qtys
    })


def login(req):
    if req.method == "POST":
        username = req.POST.get("username", '')
        password = req.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)
        if user and not user.is_staff:
            auth.login(req, user)
            messages.success(req, "You are logged in.")
            return redirect("index")
        else:
            messages.error(req, "Invalid credentials")
            return redirect(f"{reverse('login')}?username={username}")
    else:
        return render(req, 'login.html', {'values': req.GET})


def register(req):
    if req.method == "POST":
        phone_number = req.POST.get("phone_number", '')
        address = req.POST.get("address", '')
        username = req.POST.get("username", '')
        email = req.POST.get("email", '')
        password = req.POST.get("password", '')
        password2 = req.POST.get("password2", '')
        return_string = f"{reverse('register')}?username={username}&email={email}&phone_number={phone_number}&address={address}"
        # Password matches validation
        if password != password2:
            messages.error(req, "Passwords do not match!")
            return redirect(return_string)

        # Username unique validation
        elif User.objects.filter(username=username).exists():
            messages.error(req, "Username already exists!")
            return redirect(return_string)

        # Email unique validation
        elif User.objects.filter(email=email).exists():
            messages.error(req, "Email is taken!")
            return redirect(return_string)

        else:
            try:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                custom_user = CustomUser.objects.create(
                    user=user, phone_number=phone_number, address=address, confirm_id=random_id(18))
                send_mail(
                    "Afnaan's Kitchen Account confirmation",
                    '',
                    'afnaanskitchen.team@gmail.com',
                    [email],
                    fail_silently=False,
                    html_message=render_to_string('email_html/confirm_account.html', {
                        'url': f"{req.META['HTTP_HOST']}{reverse('confirm_account', kwargs={'account_id': custom_user.confirm_id})}"
                    })
                    )
                messages.success(
                    req, "We sent you a confirmation link. Please check your inbox.")
                return redirect("login")
            except Exception as e:
                print(e)
                messages.error(
                    req, "There was an error. Please try again.")
                return redirect(return_string)
    else:
        return render(req, "register.html", {'values': req.GET})


@login_required
def cart(req, current_user):
    items = FoodItem.objects.filter(is_available=True)
    cart_items = CartItem.objects.filter(
        user=current_user, qty__gte=1).order_by('-item')

    if Order.objects.filter(user=current_user, status='W'):
        messages.warning(
            req, 'You already have an order waiting to be confirmed.')
    if Order.objects.filter(user=current_user, status='P'):
        messages.warning(
            req, 'You already have an order being prepared.')
    if Order.objects.filter(user=current_user, status='O'):

        messages.warning(
            req, 'You already have an order being delivered.')

    if req.method == 'POST':
        return redirect('order')
    return render(req, 'cart.html', {
        'cart_items': cart_items,
        'total_qty': sum([order.qty for order in cart_items]),
        'total_price': sum([order.item.price * order.qty for order in cart_items]),
    })


@login_required
def settings(req, current_user):
    if req.method == 'POST':
        try:
            current_user.phone_number = req.POST.get('phone_number', '')
            current_user.address = req.POST.get('address', '')
            current_user.save()
            messages.success(req, 'Your settings have been updated')
        except:
            messages.error(req,
                           'There was an error while trying to save your credentials. Please try again')
    return render(req, 'settings.html', {'current_user': current_user})


@login_required
def user_orders(req, current_user):
    orders = Order.objects.filter(user=current_user)
    return render(req, 'user_orders.html', {
        'orders': orders,
    })


@login_required
def order(req, current_user):
    items = FoodItem.objects.filter(is_available=True)
    cart_items = CartItem.objects.filter(
        user=current_user, qty__gte=1).order_by('-item')
    total_price = sum(
        [cart_item.item.price*cart_item.qty for cart_item in cart_items])
    if not cart_items:
        messages.error(
            req, 'Please add items to your cart first.')
        return redirect('cart')
    if req.method == 'POST':
        phone_number = req.POST.get("phone_number", '')
        address = req.POST.get("address", '')
        description = req.POST.get("description", '')
        deliverytime = req.POST.get("deliverytime", '')
        password = req.POST.get('password', '')
        if not check_password(password, current_user.user.password):
            messages.error(req, 'Invalid password!')
            return redirect('order')
        order = Order.objects.create(user=current_user, price=total_price, order_description_dict={
            str(cart_item.item): cart_item.qty for cart_item in cart_items
        }, delivery_time=deliverytime)
        send_mail(
            f"New Order by User {current_user}",
            '',
            'afnaanskitchen.team@gmail.com',
            ['afnaanskitchen272@gmail.com'],
            fail_silently=False,
            html_message=render_to_string('email_html/order_email.html', {
                'current_user': current_user,
                'cart_items': cart_items,
                'order': order
            })
        )
        CartItem.objects.filter(user=current_user).delete()
        messages.success(
            req, 'Your order is placed. Please wait for it to be confirmed.')
        return redirect('menu')

    return render(req, 'order.html', {
        'current_user': current_user,
        'cart_items': cart_items,
        'total_qty': sum([cart_item.qty for cart_item in cart_items]),
        'total_price': total_price,
    })


def no_js(req):
    return render(req, 'no_js.html')


def cookie_disabled(req):
    return render(req, 'cookie_disabled.html')


@login_required
def logout(req, current_user):
    auth.logout(req)
    messages.success(req, "You are now logged out.")
    return redirect("index")


def confirm_account(req, account_id):
    if CustomUser.objects.filter(confirm_id=account_id, confirmed=False):
        user = CustomUser.objects.get(confirm_id=account_id)
        user.confirmed = True
        user.save()
        auth.login(req, user.user)
        return redirect('index')
    else:
        raise Http404('Not found')


def update_cart(req):
    if req.method == 'POST' and is_logged_in(req):
        data = json.loads(req.body.decode('utf-8'))
        current_user = CustomUser.objects.get(user=req.user.id)
        food_item = FoodItem.objects.get(name=data['item'])
        qty = data['qty']
        if CartItem.objects.filter(user=current_user, item=food_item):
            item = CartItem.objects.get(
                user=current_user, item=food_item)
            item.qty = qty
            item.save()
        else:
            item = CartItem.objects.create(
                user=current_user, item=food_item, qty=qty)
        return HttpResponse(f'{item.item} belonging to {item.user} successfully updated quantity to {item.qty}')
    else:
        raise Http404()


@login_required
def change_email(req, current_user):
    if req.method == 'POST':
        try:
            email = req.POST.get("email", '')

            # Email unique validation
            if User.objects.filter(email=email).exists():
                messages.error(req, "Email is taken!")
                return redirect("settings")

            # Email different from old validation
            elif current_user.user.email == email:
                return redirect('settings')

            current_user.confirm_id = random_id(18)
            send_mail(
                "Afnaan's Kitchen Change Email Address",
                '',
                'afnaanskitchen.team@gmail.com',
                [current_user.user.email],
                fail_silently=False,
                html_message=render_to_string('email_html/confirm_email_change.html', {
                    'current_user': current_user,
                    'email': email,
                    'url': f"{req.META['HTTP_HOST']}{reverse('confirm_email_change', kwargs={'confirm_id': current_user.confirm_id})}"
                })
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


def confirm_email_change(req, confirm_id):
    current_user = CustomUser.objects.filter(confirm_id=confirm_id)
    if current_user:
        current_user = current_user[0]
        current_user.user.email = current_user.new_email
        current_user.user.save()
        return redirect('settings')
    else:
        raise Http404('Not found')


@login_required
def change_password(req, current_user):
    if req.method == 'POST':
        current_password = req.POST.get("current_password", '')
        new_password = req.POST.get("current_password", '')
        new_password2 = req.POST.get("new_password2", '')
        if not check_password(current_password, current_user.user.password):
            messages.error(req, "Incorrect current password!")
            return redirect("settings")
        elif new_password != new_password2:
            messages.error(req, "Passwords do not match!")
            return redirect("settings")
        else:
            current_user.user.set_password(new_password)
            current_user.user.save()
            messages.success(req, "Passwords changed")
            auth.login(req, current_user.user)
            return redirect("settings")
