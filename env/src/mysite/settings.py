"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import mimetypes

mimetypes.add_type("image/jpg", ".jpg", True)
mimetypes.add_type("image/png", ".png", True)
mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("text/css", ".css", True)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR =  os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, "media")
SITE_CONFIG_DIR = os.path.join(BASE_DIR, "config")
LOCALE_DIR = os.path.join(BASE_DIR, "locale")
LOCALE_PATHS = ( LOCALE_DIR, )

DATETIME_INPUT_FORMATS = ['%Y/%m/%d %H:%M',]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
sk_file = open(SITE_CONFIG_DIR + '/sk.txt', 'r')
sk = sk_file.readline()
sk_file.close()
SECRET_KEY = sk

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    #email
    e_pw_file = open(SITE_CONFIG_DIR + '/email_pw.txt', 'r')
    e_pw = e_pw_file.readline()
    e_pw_file.close()
    E_PW = e_pw
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'mail.infoanalyse.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = "helpdesk@forum.asiacarnetwork.com"
    EMAIL_HOST_PASSWORD = E_PW
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = 'Forum AsiaCarNetwork <helpdesk@forum.asiacarnetwork.com>'

if DEBUG:
    ALLOWED_HOSTS = []
else:
    [ 'www.forum.asiacarnetwork.com','forum.asiacarnetwork.com','localhost', '128.199.189.150']

# Application definition
# TODO achievements
INSTALLED_APPS = [
    'account',
    'topic',
    'dashboard',
    
    
    'django.contrib.sites',
    'django_comments_xtd',
    'django_comments',
    
    'rest_framework',
    'rest_framework.authtoken',
    
     'corsheaders',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
]

#COMMENTS
SITE_ID = 1
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 5
COMMENTS_XTD_CONFIRM_EMAIL = False
COMMENTS_HIDE_REMOVED = True
COMMENTS_XTD_MODEL = 'topic.models.CustomComment'
COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order') 


# REST API
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
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#TODO CORS_ALLOWED_ORIGINS = ["https://www.asiacarnetwork.com","https://asiacarnetwork.com"]
CORS_ALLOW_ALL_ORIGINS = True

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

AUTH_USER_MODEL = "account.Account"
WSGI_APPLICATION = 'mysite.wsgi.application'
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800 # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800 # 50 MB


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
else:
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



    # Database
    # https://docs.djangoproject.com/en/3.1/ref/settings/#databases
    DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.mysql',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATICFILES_DIRS = [
    STATIC_DIR,
    MEDIA_DIR,
]
STATIC_URL = '/static/'

if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'cdn/static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'cdn/media')
    
else:
    # read AWS (SPACES) credentials
    aws_key_id_file = open(SITE_CONFIG_DIR + '/aws_key_id.txt', 'r')
    AWS_ACCESS_KEY_ID_TXT = aws_key_id_file.readline()
    aws_key_id_file.close()

    aws_s_key_file = open(SITE_CONFIG_DIR + '/aws_s_key.txt', 'r')
    AWS_SECRET_ACCESS_KEY_TXT = aws_s_key_file.readline()
    aws_s_key_file.close()

    aws_bucket_name_file = open(SITE_CONFIG_DIR + '/aws_bucket_name.txt', 'r')
    AWS_STORAGE_BUCKET_NAME_TXT = aws_bucket_name_file.readline()
    aws_bucket_name_file.close()

    aws_endpoint_file = open(SITE_CONFIG_DIR + '/aws_endpoint.txt', 'r')
    AWS_S3_ENDPOINT_URL_TXT = aws_endpoint_file.readline()
    aws_endpoint_file.close()

    aws_loc_file = open(SITE_CONFIG_DIR + '/aws_loc.txt', 'r')
    AWS_LOCATION_TXT = aws_loc_file.readline()
    aws_loc_file.close()

    AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID_TXT
    AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY_TXT
    AWS_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME_TXT
    AWS_S3_ENDPOINT_URL = AWS_S3_ENDPOINT_URL_TXT
    AWS_LOCATION = AWS_LOCATION_TXT
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_OBJECT_PARAMETERS = {
    'ACL': 'public-read',
    }

    

#require login to post comments
COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'default': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
        'who_can_post': 'users'
    }
}
