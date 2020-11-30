from os import path

from django.conf import settings
from django.core.management.commands.startapp import Command as BaseCommand


class Command(BaseCommand):
    """Set custom template for all newly generated apps"""
    def handle(self, **options):
        if 'template' not in options or options['template'] is None:
            options['template'] = path.join(settings.BASE_DIR, '.django-app-template')

        super().handle(**options)
