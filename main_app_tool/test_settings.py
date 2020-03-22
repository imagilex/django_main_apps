from .settings import *

try:
    test = ms.SECRET_KEY
    test = ms.ALLOWED_HOSTS[0]
    test = ms.DEBUG
    test = ms.DATABASES(os, '')
except ImportError:
    import main_app_tool.test_main_settings as ms

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
