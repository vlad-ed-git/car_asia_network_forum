"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR =  os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, "media")
SITE_CONFIG_DIR = os.path.join(BASE_DIR, "config")
LOCALE_DIR = os.path.join(BASE_DIR, "locale")
LOCALE_PATHS = ( LOCALE_DIR, )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
sk_file = open(SITE_CONFIG_DIR + '/sk.txt', 'r')
sk = sk_file.readline()
sk_file.close()
SECRET_KEY = sk

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    #TODO specify email settings
    EMAIL_HOST = "smtp.mail.com"
    EMAIL_PORT = "587"
    EMAIL_HOST_USER = "alias@mail.com"
    EMAIL_HOST_PASSWORD = "yourpassword"
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = "Helpdesk <forum_help@carasianetwork>"

INSTALLED_APPS = [
    'account',
    'website',
    'blog',
    'topic',
    'achievements',

    'django.contrib.sites',
    'django_comments_xtd',
    'django_comments',

    'rest_framework',
    'rest_framework.authtoken',

    'django.contrib.postgres',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# comments-xtd app settings
SITE_ID = 1
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 5
COMMENTS_XTD_CONFIRM_EMAIL = False
COMMENTS_HIDE_REMOVED = True
COMMENTS_XTD_MODEL = 'topic.models.CustomComment'
COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order') 

AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.AllowAllUsersModelBackend', 
    'account.backends.CaseInsensitiveModelBackend',
    )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
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

#specify custom user model
AUTH_USER_MODEL = "account.Account"
WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
dn_file = open(SITE_CONFIG_DIR + '/db_name.txt', 'r')
DB_NAME = dn_file.readline()
dn_file.close()

# set the user name
un_file = open(SITE_CONFIG_DIR + '/db_user.txt', 'r')
USER_NAME = un_file.readline()
un_file.close()

# set the password
pw_file = open(SITE_CONFIG_DIR + '/db_pw.txt', 'r')
PW = pw_file.readline()
pw_file.close()

# set the port
port_file = open(SITE_CONFIG_DIR + '/db_port.txt', 'r')
PORT = port_file.readline()
port_file.close()


# set the host
hst_file = open(SITE_CONFIG_DIR + '/db_host.txt', 'r')
HOST = hst_file.readline()
hst_file.close()

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': USER_NAME,
        'PASSWORD': PW,
        'HOST': HOST,
        'PORT': PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

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

LANGUAGE_CODE = 'th' #'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if not DEBUG:
    SECURE_SSL_REDIRECT = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATICFILES_DIRS = [
    STATIC_DIR,
    MEDIA_DIR,
]


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')


#require login to post comments
COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'default': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
        'who_can_post': 'users'
    }
}