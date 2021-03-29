"""
Django settings for chess_new_gen project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import dj_database_url
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_ALL_APP_PATH = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)
print(BASE_ALL_APP_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    '^e!tl*(m!30piznn9fy$$hfqbbhhg9h-&6i0u6r7h=345+)%x(')
if os.environ.get('ENV') == 'PRODUCTION':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'chess-app-gui.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'chess_app.apps.ChessAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "chat_public",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'free_chess_gui.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'chess_app/templates',
                 BASE_DIR / 'auth/templates',
                 BASE_DIR / 'chat_public/templates',
                 BASE_ALL_APP_PATH / 'templates'],
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

WSGI_APPLICATION = 'free_chess_gui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # on utilise l'adaptateur postgresql
        'NAME': 'chess_platform',
        # le nom de notre base de données créée précédemment

        'USER': 'anthony',


        # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': 'azerty',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'chess_app/static'),
                    os.path.join(BASE_DIR, 'auth/static'),
                    os.path.join(BASE_DIR, 'chat_public/static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'media')
)

CHAT_WS_SERVER_HOST = '127.0.0.1'
CHAT_WS_SERVER_PORT = 5002
CHAT_WS_SERVER_PROTOCOL = 'ws'

X_FRAME_OPTIONS = 'SAMEORIGIN'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
if os.environ.get('ENV') == 'PRODUCTION':
    CHAT_WS_SERVER_HOST = '0.0.0.0'
    CHAT_WS_SERVER_PORT = 5002
    CHAT_WS_SERVER_PROTOCOL = 'ws'
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
    print(STATIC_ROOT)
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    )
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
