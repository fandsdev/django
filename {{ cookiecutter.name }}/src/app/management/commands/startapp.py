from django.conf import settings
from django.core.management.commands.startapp import Command as BaseCommand


class Command(BaseCommand):
    """Set custom template for all newly generated apps"""

    def handle(self, **options):
        if "directory" not in options or options["directory"] is None:
            directory = settings.SRC_DIR / options["name"]

            directory.mkdir(exist_ok=True)

            options["directory"] = str(directory)

        if "template" not in options or options["template"] is None:
            template = settings.SRC_DIR / ".django-app-template"

            options["template"] = str(template)

        super().handle(**options)

    def validate_name(self, *args, **kwargs): ...
