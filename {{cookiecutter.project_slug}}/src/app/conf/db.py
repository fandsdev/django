# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

from app.conf.environ import env

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}
