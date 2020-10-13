from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('menu', views.menu, name='menu'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('cart', views.cart, name='cart'),
    path('settings', views.settings, name='settings'),
    path('order', views.order, name='order'),
    path('no_js', views.no_js, name='no_js'),
    path('logout', views.logout, name='logout'),
    path('confirm_account/<int:account_id>',
         views.confirm_account, name='confirm_account'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('change_email', views.change_email, name='change_email'),
    path('confirm_email_change/<int:confirm_id>',
         views.confirm_email_change, name='confirm_email_change'),
    path('change_password', views.change_password, name='change_password'),
]
