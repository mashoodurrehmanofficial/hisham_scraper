"""
Django settings for PROJECT project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os,django,json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aqu6tt=oo+fmq$y5cj^zl9tp-9y)&v9)i3g$*1b8r1)#gwb-wz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'root'
    
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

ROOT_URLCONF = 'PROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
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

WSGI_APPLICATION = 'PROJECT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases



dir_path = os.path.dirname(os.path.realpath(__file__))
credentials = json.loads(open(  os.path.join(dir_path,"credentials.json")  ,'r').read())
database_ip       = credentials['host']
database_username = credentials['username']
database_password = credentials['password']
database_name     = credentials['database'] 






DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
    'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': database_name,                      # Or path to database file if using sqlite3.
            'USER': database_username,                      # Not used with sqlite3.
            'PASSWORD': database_password,                  # Not used with sqlite3.
            'HOST': database_ip,                      # Set to empty string for localhost. Not used with sqlite3.
            # 'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    # 'default': {
    #         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    #         'NAME': 'test',                      # Or path to database file if using sqlite3.
    #         'USER': 'root',                      # Not used with sqlite3.
    #         'PASSWORD': '',                  # Not used with sqlite3.
    #         'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
    #         # 'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    #     }

}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/Static/' 
STATIC_ROOT = ''


 
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'Static')
# ]
# git config --global user.email "mashoodurrehmanofficial.com".
MEDIA_URL = '/Media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'Media')

DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'


DATE_INPUT_FORMATS = ('%m/%d/%Y',)


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

