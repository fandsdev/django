from datetime import timedelta

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(days=14),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=21),
    'JWT_ALLOW_REFRESH': True,
}
