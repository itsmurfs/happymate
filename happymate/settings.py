from __future__ import absolute_import
# ^^^ The above is required if you want to import from the celery
# library. If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.

# Celery settings
from celery.schedules import timedelta

CELERYBEAT_SCHEDULE = {
    'run_expiration_check': {
        'task': 'happyfridge.tasks.run_expiration_check',
        'schedule': timedelta(seconds=30),
        # args is used to pass arguments to the backend task
        #'args': (16, 16),
    },
}

BROKER_URL = 'amqp://guest@localhost//'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

"""
Django settings for happymate project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_l(zdhvsqwmr*kwd(+imtnn*(^j%elxj3l#0ip9xm6^2@v2++t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#Used in conjunction with debug to activate the debug flag inside template
#see https://docs.djangoproject.com/en/1.6/ref/templates/api/#django-core-context-processors-debug
INTERNAL_IPS = '127.0.0.1'

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
    'django.contrib.admin',
    'happyfridge',
    'happymate',
    'south',
    'common',
    'djcelery',
    'rest_framework',
    'rest_framework.authtoken',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'happymate.urls'

WSGI_APPLICATION = 'happymate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
PROFILE_IMG_PATH = r'C:\Windows\Users\snowpunk'
LOGIN_URL = 'account/login'
ACCOUNT_LINK_BASE_URL = 'http://127.0.0.1:8000'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'happymate@happymate.itsmurfs.it'
#EMAIL_HOST_PASSWORD = 'happymate_activation_link'
