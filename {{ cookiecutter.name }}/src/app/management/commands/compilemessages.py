from pathlib import Path
from typing import Any

import polib
from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """Compile .po catalogues in LOCALE_PATHS with polib, so GNU gettext is not needed"""

    help = "Compiles .po files to .mo files for use with builtin gettext support."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--locale", "-l", action="append", default=[], help="Locale(s) to process. Default is to process all.")

    def handle(self, *args: Any, **options: Any) -> None:
        for locale_path in settings.LOCALE_PATHS:
            for po_file in sorted(Path(locale_path).glob("*/LC_MESSAGES/*.po")):
                if options["locale"] and po_file.parent.parent.name not in options["locale"]:
                    continue

                if options["verbosity"] > 0:
                    self.stdout.write(f"processing file {po_file.name} in {po_file.parent}")

                polib.pofile(str(po_file)).save_as_mofile(str(po_file.with_suffix(".mo")))
