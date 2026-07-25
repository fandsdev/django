import contextlib
import importlib

from django.apps.config import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    """Default App configuration template. Imports app.signals.handlers.

    We do not recommend you to use django signals at all.
    Check out https://lincolnloop.com/blog/django-anti-patterns-signals/ if
    you know nothing about that.

    Although, if you wish to use signals, place handlers to the `signals/handlers.py`:
    your code will be automatically imported and used.
    """

    # Django's `apps.py` scan sees two configs — yours and this one, pulled in by your import.
    # `False` here, `True` in your subclass: otherwise Django silently takes a plain AppConfig.
    default = False

    def ready(self) -> None:
        """Import a module with handlers if it exists to avoid boilerplate code."""
        with contextlib.suppress(ModuleNotFoundError):
            importlib.import_module(".signals.handlers", self.module.__name__)  # type: ignore[union-attr]
