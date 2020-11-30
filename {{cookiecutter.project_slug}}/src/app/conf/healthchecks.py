# Django Healthchecks
# http://django-healthchecks.readthedocs.io

HEALTH_CHECKS_ERROR_CODE = 503
HEALTH_CHECKS = {
    'db': 'django_healthchecks.contrib.check_database',
}
