"""
Django settings for main_app_tool project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import mimetypes
import os

import main_app_tool.main_settings as ms

mimetypes.add_type('text/css', '.css', True)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ms.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ms.DEBUG

ALLOWED_HOSTS = ms.ALLOWED_HOSTS

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'django.contrib.humanize',

    'zend_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main_app_tool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "html_templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'main_app_tool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = ms.DATABASES(os, BASE_DIR)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = False

EMAIL_HOST = ms.EMAIL_SETTINGS['EMAIL_HOST']
EMAIL_PORT = ms.EMAIL_SETTINGS['EMAIL_PORT']
EMAIL_HOST_USER = ms.EMAIL_SETTINGS['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = ms.EMAIL_SETTINGS['EMAIL_HOST_PASSWORD']
EMAIL_USE_SSL = ms.EMAIL_SETTINGS['EMAIL_USE_SSL']
DEFAULT_FROM_EMAIL = ms.EMAIL_SETTINGS['DEFAULT_FROM_EMAIL']

FILE_UPLOAD_MAX_MEMORY_SIZE = 8400000
DATA_UPLOAD_MAX_MEMORY_SIZE = 5250000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2500

LOGIN_URL = 'session_login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

if DEBUG is False:
    STATIC_ROOT = os.path.join('/home/#USER#/public_html/', 'static/')
    MEDIA_ROOT = os.path.join('/home/#USER#/public_html/', 'media/')
    # STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'files/static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'files/media')
