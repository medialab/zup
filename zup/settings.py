#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django settings for zup project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import local_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xe$0js2h%k*mc#erl6rx97)kra8(8)gftuwee24b+=4=*o+v#b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.DEBUG

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'zup'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'zup.urls'

WSGI_APPLICATION = 'zup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': local_settings.DB_ENGINE,
        'NAME': local_settings.DB_NAME,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = local_settings.LANGUAGE_CODE

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


TITLE = local_settings.TITLE
STATIC_URL = local_settings.STATIC_URL
STATIC_ROOT = local_settings.STATIC_ROOT
MEDIA_ROOT = local_settings.MEDIA_ROOT
MEDIA_URL = local_settings.MEDIA_URL

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'src'),
)

TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, 'templates'),
)

ENABLE_CDN_SERVICES = local_settings.ENABLE_CDN_SERVICES

PYTHON_INTERPRETER = local_settings.PYTHON_INTERPRETER

EN = 'en'
IT = 'it'
FR = 'fr'
NL = 'nl'

LANGUAGE_CHOICES = (
  (EN, u'english'),
  (FR, u'french'),
  (NL, u'dutch'),
  (IT, u'italian'),
)