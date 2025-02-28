"""
Django settings for type2speed project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# import environ

# # Initialise environment variables
# env = environ.Env()
# environ.Env.read_env()  # This reads the .env file

# # Set DEBUG based on the environment variable
# DEBUG = env.bool("DEBUG", default=True) 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6qjf&&25x0#orvqj&bev2jw9nu_6-!k*saw2g6pzj&9732&j0u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['139.59.38.231','127.0.0.1','localhost','type2speed.com']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'typing_app',
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

ROOT_URLCONF = 'type2speed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Global templates (optional)
            os.path.join(BASE_DIR, 'typing_app', 'templates'),  # App-specific templates
        ],
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

WSGI_APPLICATION = 'type2speed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
]

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# STATIC_URL = '/static/'

# # Define where Django should collect static files for production
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# # Define additional static file directories (only if you manually put static files there)
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),  # Ensure this directory exists
# ]

STATIC_URL = '/static/'

# Directory where `collectstatic` will store all static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Define additional static file directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'typing_app', 'static'),  # Ensure this directory exists
]



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




log_directory = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # File handler for Django errors (both local and production)
        'file': {
            'level': 'ERROR',  # Capture errors and higher
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_directory, 'django_error.log'),  # Path for logs
        },
        # Console handler for local development (optional)
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Django logger
        'django': {
            'handlers': ['file', 'console'],  # Both file and console for easier debugging
            'level': 'ERROR',  # Capture errors and above
            'propagate': True,
        },
        # Log for Gunicorn errors (if used)
        'gunicorn.error': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
