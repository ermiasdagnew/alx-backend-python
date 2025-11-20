import os
from pathlib import Path

# ----------------------------------------
# BASE DIRECTORY
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------
# SECURITY SETTINGS
# ----------------------------------------
SECRET_KEY = 'replace-this-with-your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

# ----------------------------------------
# INSTALLED APPS
# ----------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # project apps
    'chats',
]

# ----------------------------------------
# MIDDLEWARE SETTINGS
# ----------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom middleware
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'chats.middleware.RolepermissionMiddleware',
]

# ----------------------------------------
# ROOT URL
# ----------------------------------------
ROOT_URLCONF = 'messaging_app.urls'

# ----------------------------------------
# TEMPLATES
# ----------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ----------------------------------------
# WSGI
# ----------------------------------------
WSGI_APPLICATION = 'messaging_app.wsgi.application'

# ----------------------------------------
# DATABASE
# ----------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------------------
# PASSWORD VALIDATION
# ----------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

# ----------------------------------------
# INTERNATIONALIZATION
# ----------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------
# STATIC FILES
# ----------------------------------------
STATIC_URL = 'static/'

# ----------------------------------------
# DEFAULT PK FIELD
# ----------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
