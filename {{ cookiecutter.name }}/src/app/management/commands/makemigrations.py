from django.core.management.base import CommandError
from django.core.management.commands.makemigrations import Command as BaseCommand


class MakemigrationsError(CommandError):
    pass


class Command(BaseCommand):
    """Disable automatic names for django migrations, thanks https://adamj.eu/tech/2020/02/24/how-to-disallow-auto-named-django-migrations/"""

    def handle(self, *app_labels, **options):
        if options["name"] is None and not any([options["dry_run"], options["check_changes"]]):
            raise MakemigrationsError("Migration name is required. Run again with `-n/--name` argument and specify name explicitly.")

        super().handle(*app_labels, **options)
