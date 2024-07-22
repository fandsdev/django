import os

from celery import Celery
from django.conf import settings

__all__ = ["celery"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

celery = Celery("app")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

celery.conf.beat_schedule = {}
