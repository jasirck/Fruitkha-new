"""
Django settings for fruitkha project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ['16.170.215.41','0.0.0.0']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')


CSRF_TRUSTED_ORIGINS=['http://16.170.215.41',
'https://16.170.215.41',
'http://0.0.0.0',
'https://0.0.0.0',
'http://0.0.0.0:9090']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage",
    "login",
    "my_admin",
    "shop",
    "order",
    "account",
    "cart",
    "wallet",
    "coupon",
    "offer",
    "sales",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "login.Customer"

LOGIN_URL = "/login"

ROOT_URLCONF = "fruitkha.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "fruitkha.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "fruitkha",
        "HOST": "localhost",
        "PORT": "5432",
        "USER": "jasir",
        "PASSWORD": config("PASSWORD"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

CORS_ALLOWED_ORIGINS = [
"http://16.170.215.41",
"https://16.170.215.41",
"http://0.0.0.0",
"https://0.0.0.0",
"http://0.0.0.0:9090"]

CORS_ALLOW_HEADERS = [
                 'access-control-allow-headers',
                   'access-control-allow-methods',
                  'access-control-allow-origin',
                    'content-type',
                     'x-csrftoken']

CORS_ALLOW_METHODS = [
               'DELETE',
               'GET',
               'OPTIONS',
               'PATCH',
               'POST',
               'PUT']



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True


STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

APPEND_SLASH = False
