from .settings import *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'sql_mode': 'traditional',
        },
        'NAME': 'afnaanskitchen$akdb',
        'USER': 'afnaanskitchen',
        'PASSWORD': '************',
        'HOST': 'afnaanskitchen.mysql.pythonanywhere-services.com'
    }
}
DEBUG = False

ALLOWED_HOSTS = ['afnaanskitchen.pythonanywhere.com', 'localhost', '127.0.0.1']

