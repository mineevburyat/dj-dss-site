"""
Django settings for dss project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import environ
from pathlib import Path
# importing the function from utils
from django.core.management.utils import get_random_secret_key



root = Path(__file__).resolve().parent.parent  # get root of the project
env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, 'get_random_secret_key()'),
    ALLOWED_HOSTS=(list, ['localhost', '*']),
    PG_DB=(str,'project_bd'),
    PG_USER=(str,'pgdb_user'),
    PG_PASS=(str,'pgdb_user_pass'),
    PG_HOST=(str,'localhost'),
    PG_PORT=(str,''),
)
env.read_env(root / '.env')  # reading .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = root


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'django_json_widget',
    'django_extensions',
    # 'schedule',
    # 'djangobower',
    # 'django_jsonform',
    # 'sliderapp',
    'common',
    'home',
    'app_lk',
    'app_mediafiles',
    'menu',
    'app_objects',
    'app_services',
    'app_about',
    'app_user',
    'app_contacts',
    'app_piplscard',
    'app_shedule',
    'app_booking',
    'app_news',
    'app_tags',
    'app_search',
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

ROOT_URLCONF = 'dss.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", ],
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

WSGI_APPLICATION = 'dss.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('PG_DB'),
        'USER': env('PG_USER'),
        'PASSWORD': env('PG_PASS'),
        'HOST': env('PG_HOST'),
        'PORT': env('PG_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Irkutsk'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = [
    
    ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CK editor
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' 

CKEDITOR_CONFIGS = {
    'default':
        {
            'toolbar': 'full',
            'width': 'auto',
            'extraPlugins': ','.join([
                'codesnippet',
            ]),
        },
}

# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'djangobower.finders.BowerFinder',

# ]
BOWER_COMPONENTS_ROOT = '/home/dj-dss-site/dss/components/'
BOWER_INSTALLED_APPS = (
    'jquery',
    'jquery-ui',
    'bootstrap'
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'app_user.User'
LOGIN_URL = '/user/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log'
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            
        }
    },
    'loggers': {
            # 'django': {
            #     'handlers': ['debug_file'],
            #     'level': 'DEBUG',
            #     'propagate': True,
            # },
            '': {
                'handlers': ['error_file', ],
                'level': 'ERROR',
                'propagate': True,
            },
        },
}
# ADMINS = (
#     ('admin', 'alex@mineev03.ru'),
# )
# ...
# EMAIL_SUBJECT_PREFIX = '[DSS site] '
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_HOST_USER = 'alex@mineev03.ru'
# EMAIL_HOST_PASSWORD = 'XXXXXX'
# EMAIL_PORT = 465
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
# SERVER_EMAIL = 'alex@mineev03.ru'
# DEFAULT_FROM_EMAIL = 'alex@mineev03.ru'