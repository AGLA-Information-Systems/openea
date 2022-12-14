"""
Django settings for openea project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import configparser
from pathlib import Path
ini_config = configparser.ConfigParser()
ini_config.read('config.ini')

ENVIRONMENT = ini_config.get('DEFAULT', "ENVIRONMENT", fallback='dev')
CONTACT_EMAIL = ini_config.get('DEFAULT', "CONTACT_EMAIL", fallback='info@aglaglobal.com')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ini_config.get('DEFAULT', "SECRET_KEY", fallback='1rq154z4694=s^zza--pe@czoh^s$=y(j@y)4ws(6&0@m+ie-*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ini_config.getboolean('DEFAULT', "DEBUG", fallback=True)

#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ini_config.get('DEFAULT', "DJANGO_ALLOWED_HOSTS", fallback='*').split(" ")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'authorization.apps.AuthorizationConfig',
    'authentication.apps.AuthenticationConfig',
    'ontology.apps.OntologyConfig',
    'webapp.apps.WebappConfig',
    'taxonomy.apps.TaxonomyConfig',
    'configuration.apps.ConfigurationConfig',
    'crispy_forms',
    "crispy_bootstrap5",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'webapp.middleware.profile.ActiveProfileMiddleware',
]

ROOT_URLCONF = 'openea.urls'

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

WSGI_APPLICATION = 'openea.wsgi.application'

#CSRF_COOKIE_DOMAIN = '.openenterprisearchitect.com'
#CSRF_TRUSTED_ORIGINS = ['https://*.openenterprisearchitect.com','https://*.127.0.0.1']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": ini_config.get('Database', "SQL_ENGINE", fallback="django.db.backends.sqlite3"),
        "NAME": ini_config.get('Database', "SQL_DATABASE", fallback= BASE_DIR / "db.sqlite3"),
        "USER": ini_config.get('Database', "SQL_USER", fallback="user"),
        "PASSWORD": ini_config.get('Database', "SQL_PASSWORD", fallback="password"),
        "HOST": ini_config.get('Database', "SQL_HOST", fallback="localhost"),
        "PORT": ini_config.get('Database', "SQL_PORT", fallback="5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = Path(BASE_DIR, 'static')
STATIC_URL = '/static/'

### ================================================================================
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MEDIA_ROOT = Path(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             'format': '%(name)-12s %(levelname)-8s %(message)s'
#         },
#         'file': {
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
#         }
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'formatter': 'file',
#             'filename': '/tmp/debug.log'
#         }
#     },
#     'loggers': {
#         '': {
#             'level': 'DEBUG',
#             'handlers': ['console', 'file']
#         }
#     }
# }

LANGUAGES = [
  ('en-us', 'English'),
  ('fr', 'French'),
  ('es', 'Spanish'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
