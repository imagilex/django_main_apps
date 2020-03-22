
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'th1$!$t43$3c1237k34'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

EMAIL_SETTINGS = {
        'EMAIL_HOST': 'mail.domain.com',
        'EMAIL_PORT': '465',
        'EMAIL_HOST_USER': 'correo@domain.com',
        'EMAIL_HOST_PASSWORD': 'p@$$m0r9',
        'EMAIL_USE_SSL': True,
        'DEFAULT_FROM_EMAIL': 'Sistemas<no-reply@domain.com>',
    }


def DATABASES(os, BASE_DIR):
    db = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'managed/db_test.imgx'),
        }
    }
    return db
