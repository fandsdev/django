from app.conf.environ import env

ALLOWED_HOSTS = ['*']  # host validation is not necessary in 2020
CSRF_TRUSTED_ORIGINS = [
    'your.app.origin',
]

if env('DEBUG'):
    ABSOLUTE_HOST = 'http://localhost:3000'
else:
    ABSOLUTE_HOST = 'https://your.app.com'
