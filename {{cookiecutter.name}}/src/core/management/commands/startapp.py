from pathlib import Path

from django.conf import settings
from django.core.management.commands.startapp import Command as BaseCommand


class Command(BaseCommand):
    """Set custom template for all newly generated apps"""

    def handle(self, **options):
        if "template" not in options or options["template"] is None:
            options["template"] = str(Path(settings.BASE_DIR).parent / ".django-app-template")

        super().handle(**options)

        testsdir = Path(settings.BASE_DIR).parent.parent / "tests" / "apps" / options["name"]
        testsdir.mkdir(parents=True, exist_ok=True)

        (testsdir / "__init__.py").touch()
        (testsdir / "factory.py").touch()
        (testsdir / "fixtures.py").touch()
