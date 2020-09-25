from django.shortcuts import render


def index(req):
    return render(req, 'index.html')


def about(req):
    return render(req, 'about.html')


def menu(req):
    return render(req, 'menu.html')


def login(req):
    return render(req, 'login.html')


def register(req):
    return render(req, 'register.html')
