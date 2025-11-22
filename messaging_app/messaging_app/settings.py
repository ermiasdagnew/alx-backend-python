from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-me-task4'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'chats',
]

MIDDLEWARE = [
    ...
    'chats.middleware.RequestLoggingMiddleware',
    ...
]


ROOT_URLCONF = 'messaging_app.urls'
WSGI_APPLICATION = 'messaging_app.wsgi.application'

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3
