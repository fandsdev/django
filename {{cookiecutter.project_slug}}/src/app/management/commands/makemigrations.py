import sys

from django.core.management.commands.makemigrations import Command as BaseCommand


class Command(BaseCommand):
    """Disable automatic names for django migrations, thanks https://adamj.eu/tech/2020/02/24/how-to-disallow-auto-named-django-migrations/
    """
    def handle(self, *app_labels, **options):
        if options['name'] is None and not any([options['dry_run'], options['check_changes']]):
            print('Migration name (-n/--name) is required.', file=sys.stderr)  # noqa: T001
            sys.exit(1)

        super().handle(*app_labels, **options)
