#
# This file was generated using http://github.com/f213/django starter template.
#
# If your project growth to more then 3 apps, consider http://github.com/sobolevn/django-split-settings
# for organizing django settings into multiple files
#
import os

import environ

root = environ.Path(__file__) - 2        # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()                   # reading .env file
SITE_ROOT = root()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Disable built-in ./manage.py test command in favor of pytest
TEST_RUNNER = 'app.test.disable_test_command_runner.DisableTestCommandRunner'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', cast=bool, default=False)
CI = env('CI', cast=bool, default=False)

ALLOWED_HOSTS = ['*']  # host validation is not necessary in 2020


# Application definition

INSTALLED_APPS = [
    'app',
    'users',
    'sepulkas',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_jwt.blacklist',
    'django_filters',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'app.urls'
AUTH_USER_MODEL = 'users.User'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = ['locale']
TIME_ZONE = 'UTC'
USE_L10N = True
USE_i18N = True
USE_TZ = True


# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/

MAX_PAGE_SIZE = env('MAX_PAGE_SIZE', cast=int, default=1000)
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'app.renderers.AppJSONRenderer',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'app.pagination.AppPagination',
    'PAGE_SIZE': env('PAGE_SIZE', cast=int, default=20),
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = env('STATIC_ROOT', cast=str, default='static')

if not DEBUG and not CI:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')


# Sentry
# https://sentry.io/for/django/
SENTRY_DSN = env('SENTRY_DSN', cast=str, default='')
if not DEBUG and len(SENTRY_DSN):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
    )


# Django Healthchecks
# http://django-healthchecks.readthedocs.io

HEALTH_CHECKS_ERROR_CODE = 503
HEALTH_CHECKS = {
    'db': 'django_healthchecks.contrib.check_database',
}
