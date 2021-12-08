from datetime import timedelta

from app.conf.environ import env

AUTH_USER_MODEL = 'users.User'
AXES_ENABLED = env('AXES_ENABLED', cast=bool, default=True)

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(days=14),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=21),
    'JWT_ALLOW_REFRESH': True,
}


#
# Security notice: we use plain bcrypt to store passwords.
#
# We avoid django default pre-hashing algorithm
# from contrib.auth.hashers.BCryptSHA256PasswordHasher.
#
# The reason is compatibility with other hashing libraries, like
# Ruby Devise or Laravel default hashing algorithm.
#
# This means we can't store passwords longer then 72 symbols.
#

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
