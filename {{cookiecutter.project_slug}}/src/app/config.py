import importlib

from django.apps.config import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    """Default App configuration template. Import app.signals.handers.

    We do not recomend you to use django signals at all.
    Check out https://lincolnloop.com/blog/django-anti-patterns-signals/ if you know nothing about it.
    Allthough, if you wish to use signals, place handlers to the `signals/handlers.py`:
    your code be automatically imported and used.
    """
    def ready(self):
        """Import a module with handlers if it exists to avoid boilerplate code."""
        try:
            importlib.import_module('.signals.handlers', self.module.__name__)
        except ModuleNotFoundError:
            pass
