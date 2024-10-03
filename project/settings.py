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
CSRF_TRUSTED_ORIGINS=['https://itnb.up.railway.app']

WEBSITE_URL='http://localhost:5173'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(config('REDIS_URL'))],
        },
    },
}


DJANGO_REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Number of properties per page
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
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
    "ALGORITHM": "HS512",
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'  # Specify the username field
ACCOUNT_USERNAME_REQUIRED = True                 # Make username required
ACCOUNT_AUTHENTICATION_METHOD = 'email'          # Authentication via email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'             
AUTH_USER_MODEL = 'useraccount.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


#--------------------------------------------------------------------------------------
# Application definition :
INSTALLED_APPS = [
    'corsheaders',
    'channels',
    'daphne',
    'useraccount',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Other apps for authintication :)
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account', 
    'allauth.socialaccount',  
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'drf_yasg',

    'django_filters',
    'cloudinary',
    'cloudinary_storage',
    # project main apps
    'property',
    'Reservation' ,
    'chat',
    'reviews_and_ratings',
    'payments',
    'favorite',
]




#--------------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------------
# Email Configuration to send massages from your acount to the useres :)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')  
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',  # Change to 'INFO' or 'WARNING' in production
#         },
#     },
# }

#--------------------------------------------------------------------------------------

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000', 
    'http://127.0.0.1:3000', 
    'http://localhost:5173',
    'https://itnb.up.railway.app',
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

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_ALL_ORIGINS = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add your templates directory here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'useraccount.context_processors.website_url',  

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
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

# payment settings
PAYMOB_API_KEY = 'ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2T1RrMk5ETTJMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuWnc2WEcyVGYybkxSNE83b0wwai1Ea1FESzVFYlNaSVh5dFBTLUNSZHpkQTk1V29RRjYzTlQ0SFRmeFRjMWZ4SHNKWVB4WERtVXJKVjBzMHZtY3VILVE='
PAYMOB_INTEGRATION_ID = '4836448'


