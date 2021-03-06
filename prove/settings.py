"""
Django settings for prove project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$u*%4(k6(kos_04ox3m$@0b8r@laig5u+b^1ywp7ry&im3ud8o'
PLATFORM_CONFIG_NAME = "prove.conf"

production_config = os.path.join('/etc', 'prove', PLATFORM_CONFIG_NAME)
development_config = os.path.join(BASE_DIR, PLATFORM_CONFIG_NAME)

config_path = production_config if os.path.exists(production_config) else development_config
config = ConfigParser()
config.read(config_path)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('common', 'debug', fallback=True)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'landing',
    'payment',
    'user',
    'course',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.AuthMiddleware'

]
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}

ROOT_URLCONF = 'prove.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'prove.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'ENGINE', fallback='django.db.backends.mysql'),
        'NAME': config.get('database', 'NAME', fallback='prove'),
        'USER': config.get('database', 'USER', fallback='prove'),
        'PASSWORD': config.get('database', 'PASSWORD', fallback='prove'),
        'HOST': config.get('database', 'HOST', fallback='127.0.0.1'),
        'PORT': config.getint('database', 'PORT', fallback=3306),
        'TEST_CHARSET': 'utf8mb4'
    }
}
MERCHANT_LOGIN = config.get('robokassa', 'LOGIN', fallback='prokrutyh')
PASSWORD1 = config.get('robokassa', 'PASSWORD1', fallback='')
PASSWORD2 = config.get('robokassa', 'PASSWORD2', fallback='')
SECRET_HASH = config.get('common', 'SECRET_HASH', fallback='')
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = config.get('common', 'STATIC_ROOT', fallback='/opt/prove-back/static/')

VK_CLIENT_ID = config.get('oauth', 'vk_client_id', fallback='')
REDIRECT_URL = config.get('oauth', 'redirect_url', fallback='http://prove-project.ru/api/user/vk-auth')
VK_CLIENT_SECRET = config.get('oauth', 'vk_secret', fallback='')

FB_CLIENT_ID = config.get('oauth', 'fb_client_id', fallback='')
FB_REDIRECT_URL = config.get('oauth', 'fb_redirect_url', fallback='http://prove-project.ru/api/user/fb-auth')
FB_CLIENT_SECRET = config.get('oauth', 'fb_secret', fallback='')

