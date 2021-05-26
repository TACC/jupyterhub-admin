"""
Django settings for jupyterhub_admin project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import logging
from django.core.management.utils import get_random_secret_key


logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None) 
if not SECRET_KEY:
    logger.warning("Missing DJANGO_SECRET_KEY environment variable. Generating random secret key.")
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

# Token used for JupyterHub access
JUPYTERHUB_TOKEN = os.environ.get('JUPYTERHUB_TOKEN', None)
if not JUPYTERHUB_TOKEN:
    logger.warning("Missing JUPYTERHUB_TOKEN environment variable")

# API URL for JupyterHub
JUPYTERHUB_SERVER = os.environ.get('JUPYTERHUB_SERVER', None)
if not JUPYTERHUB_SERVER:
    logger.warning("Missing JUPYTERHUB_API environment variable")

TENANT = os.environ.get('TENANT', None)
if not TENANT:
    logger.warning("Missing TENANT environment variable")

INSTANCE = os.environ.get('INSTANCE', None)
if not TENANT:
    logger.warning("Missing INSTANCE environment variable")

# Agave API for Metadata
AGAVE_API = os.environ.get('AGAVE_API', None)
if not AGAVE_API:
    logger.warning("Missing AGAVE_API environment variable")

# Agave token for Jupyterh account
AGAVE_SERVICE_TOKEN = os.environ.get('AGAVE_SERVICE_TOKEN', None)
if not AGAVE_SERVICE_TOKEN:
    logger.warning("Missing AGAVE_SERVICE_TOKEN environment variable")

# Agave login client key and secret
AGAVE_CLIENT_KEY = os.environ.get('AGAVE_CLIENT_KEY', None)
AGAVE_CLIENT_SECRET = os.environ.get('AGAVE_CLIENT_SECRET', None)
if not AGAVE_CLIENT_KEY or not AGAVE_CLIENT_SECRET:
    logger.warning("Missing AGAVE_CLIENT_KEY or AGAVE_CLIENT_SECRET environment variable")

ALLOWED_HOSTS = ['*']


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jupyterhub_admin.apps.jupyterhub',
    'jupyterhub_admin.apps.main',
    'jupyterhub_admin.apps.images',
    'jupyterhub_admin.apps.mounts',
    'jupyterhub_admin.apps.agaveauth',
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

ROOT_URLCONF = 'jupyterhub_admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'jupyterhub_admin/templates')],
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

WSGI_APPLICATION = 'jupyterhub_admin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}