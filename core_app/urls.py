from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('menu', views.menu, name='menu'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('confirm_account/<int:account_id>',
         views.confirm_account, name='confirm_account'),
    path('cart', views.cart, name='cart'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('settings', views.settings, name='settings'),
    path('logout', views.logout, name='logout'),
    path('change_password', views.change_password, name='change_password'),
    path('change_email', views.change_email, name='change_email'),
    path('change_user_email/<int:confirm_id>', views.change_user_email, name='change_user_email'),
]
