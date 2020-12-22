import os
from config.utils import EnviromentVariable

EVARS = EnviromentVariable()

BASE_DIR = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            )
SECRET_KEY = EVARS.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = EVARS.DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    'mscore',
    'dialogs',
    'messages',
    'files',
    'relations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'mscore.middlewares.AuthMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': EVARS.DB_HOST,
        'NAME': EVARS.DB_NAME,
        'USER': EVARS.DB_USER,
        'PASSWORD': EVARS.DB_PASS,
    },
}


# DATABASE_ROUTERS = ['mail.db_router.AppLevelDatabaseRouter',]


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'mscore.authentication.SessionAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

#CUSTOM SETTINGS
API_INSTANCE_SENDERS = {
}

API_INSTANCE_DEPENDENCIES = {
    'accounts.users.user': 'relations.models.UserRelationModel',
}

USER_RELATION_MODEL = 'relations.models.UserRelationModel'

API_END_POINT_URL = EVARS.API_ENDPOINT_URL

API_TOKEN = EVARS.INSTANCE_TOKEN

APPEND_NAMESPACES_TO_URLNAME = False
