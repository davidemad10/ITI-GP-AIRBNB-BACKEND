"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import dj_database_url
import os
from decouple import config
from pathlib import Path
from datetime import timedelta
import cloudinary_storage
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config


DEBUG = True


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-z^0zbvvg*ap3wt#^8bo9xblpl_r&hvsn56s1odspv!bldvx3#g' 
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['.vercel.app']
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = ['*']


WEBSITE_URL='http://localhost:8000'

CHANNEL_LAYERS={
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

DJANGO_REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
       'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # Add any other authentication backends you're using
]


SITE_ID = 1

REST_USE_JWT = True
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKEN": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": "acomplexkey",
    "ALOGRIGTHM": "HS512",
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'  # Specify the username field
ACCOUNT_USERNAME_REQUIRED = True                 # Make username required
ACCOUNT_AUTHENTICATION_METHOD = 'email'          # Authentication via email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'              # As per your current settings
AUTH_USER_MODEL = 'useraccount.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# Application definition

INSTALLED_APPS = [
    'channels',
    'daphne',
    'useraccount',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    
    # Other apps for authintication :)
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account', 
    'allauth.socialaccount',  
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'drf_yasg',


    # project main apps
    'property',
    'Reservation' , 
    'django_filters',
    
    'chat',

    'cloudinary',
    'cloudinary_storage',
    
    'reviews_and_ratings',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 

]


CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000', 
    'http://127.0.0.1:3000', 
    'http://localhost:5173',
]



CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CORS_ALLOW_ALL_ORIGINS = True



ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = 'project.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DB_SELECTION = config('DB_SELECTION', default='PROD')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PGDATABASE'),
        'USER': config('PGUSER'),
        'PASSWORD': config('PGPASSWORD'),
        'HOST': config('PGHOST'),
        'PORT': config('DB_PORT'),
    }
}


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

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


cloudinary.config( 
    cloud_name = "dt0nlcc8n", 
    api_key = "571797429827582", 
    api_secret = "wG8DNq45p9FvvJbMPokTgTExpiY",
    secure = True
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dt0nlcc8n',
    'API_KEY': '571797429827582',
    'API_SECRET': 'wG8DNq45p9FvvJbMPokTgTExpiY',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

OPENCAGE_API_KEY = config('OPENCAGE_API_KEY')


