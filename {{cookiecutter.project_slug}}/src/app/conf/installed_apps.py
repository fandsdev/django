# Application definition

APPS = [
    'app',
    'a12n',
    'users',
]

THIRD_PARTY_APPS = [
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_jwt.blacklist',
    'django_filters',
    'axes',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = APPS + THIRD_PARTY_APPS
