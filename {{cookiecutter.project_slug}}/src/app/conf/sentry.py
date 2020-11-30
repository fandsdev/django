from app.conf.environ import env

# Sentry
# https://sentry.io/for/django/

SENTRY_DSN = env('SENTRY_DSN', cast=str, default='')

if not env('DEBUG') and len(SENTRY_DSN):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
    )
