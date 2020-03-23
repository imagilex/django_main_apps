"""
Configuraciones de trabajo para pruebas unitarias y funcionales
a ejecutar con pytest

Se hace una importacion de settings.py
Se redefinen los parametros:
 - DATABASES
 - EMAIL_BACKEND
"""

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
