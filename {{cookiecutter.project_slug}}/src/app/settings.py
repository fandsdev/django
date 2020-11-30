# This file was generated using http://github.com/f213/django starter template.
#
# Settings are split into multiple files using http://github.com/sobolevn/django-split-settings

from split_settings.tools import include

from app.conf.environ import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', cast=bool, default=False)
CI = env('CI', cast=bool, default=False)

include(
    'conf/api.py',
    'conf/auth.py',
    'conf/boilerplate.py',
    'conf/db.py',
    'conf/healthchecks.py',
    'conf/http.py',
    'conf/i18n.py',
    'conf/installed_apps.py',
    'conf/media.py',
    'conf/middleware.py',
    'conf/storage.py',
    'conf/sentry.py',
    'conf/static.py',
    'conf/templates.py',
    'conf/timezone.py',
)
