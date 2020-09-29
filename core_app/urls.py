from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('menu', views.menu, name='menu'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('confirm_account/<int:account_id>', views.confirm_account, name='confirm_account'),
]
