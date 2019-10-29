import sys, os
from base64 import b64encode
import netifaces
import requests
import binascii
from time import sleep
from .my_stuff import *

# for info, imported from my_stuff
PRODUCTION = PRODUCTION
print(f'PRODUCTION = {PRODUCTION}')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR = {}".format(BASE_DIR))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = binascii.hexlify(os.urandom(50)).decode("utf-8")
print(f'SECRET_KEY = {SECRET_KEY}')

#>>>> PRODUCTION ADJUSTMENT
# if PRODUCTION == True:
#     SECRET_KEY = binascii.hexlify(os.urandom(25)).decode("utf-8")
#     print(SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#>>>> PRODUCTION ADJUSTMENT
if PRODUCTION == True:
    DEBUG = DEBUG_PROD # imported
print(f'DEBUG is: {DEBUG}')

# only info, imported
PROXY_IPS = PROXY_IPS

PRODUCTION_IP = PRODUCTION_IP.replace('http://', '') # only info, is imported
print(f'PRODUCTION_IP = {PRODUCTION_IP}')
ALLOWED_HOSTS = []
if PRODUCTION == True:
    ALLOWED_HOSTS.extend(PROXY_IPS)
    ALLOWED_HOSTS.append(PRODUCTION_IP)
else:
    ALLOWED_HOSTS.append('localhost')
print(f'ALLOWED_HOSTS are: {ALLOWED_HOSTS}')

PROXIES = {
            'http': os.environ.get('http_proxy'),
            'https': os.environ.get('https_proxy'),
            'ftp': os.environ.get('ftp_proxy'),
            'socks': os.environ.get('socks_proxy'),
            }

# Application definition
INSTALLED_APPS = [
                    'chess.apps.ChessConfig',
                    'config.apps.ConfigConfig',
                    'blog.apps.BlogConfig',
                    'users.apps.UsersConfig',
                    'crispy_forms',
                    'django.contrib.admin',
                    'django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions',
                    'django.contrib.messages',
                    'django.contrib.staticfiles',
                    'rest_framework',
                ]
#>>>> PRODUCTION ADJUSTMENT
if PRODUCTION == True:
    INSTALLED_APPS.append('mod_wsgi.server')
    print(f'INSTALLED_APPS: {INSTALLED_APPS}')

MIDDLEWARE = [
                'django.middleware.security.SecurityMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware',
                'web_project.auth_middleware.LoginRequiredMiddleware'
            ]

ROOT_URLCONF = 'web_project.urls'

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

WSGI_APPLICATION = 'web_project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '122_chess_play.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'de-DE'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
print(f"STATIC_ROOT: {STATIC_ROOT}")
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
print(f"MEDIA_ROOT: {MEDIA_ROOT}")

ACCOUNT_ACTIVATION_DAYS = 2
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'
LOGIN_NOT_REQUIRED = (r'blog/posts/Theme=0/Article=0/Post=0/Frame=0/view/',
                        r'blog/articles/Theme=0/Article=0/Frame=0/view/',
                        r'')
LOGIN_FORBIDDEN = (r'users/login/', r'users/register/',)

# mail params for signin and password recovery
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# inly info all these fields are imported
EMAIL_HOST = EMAIL_HOST
EMAIL_PORT = EMAIL_PORT
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD

# addon allowes chess app to quit process when button is pressed
CHPID = os.getpid()
print(f"CHPID: {CHPID}")