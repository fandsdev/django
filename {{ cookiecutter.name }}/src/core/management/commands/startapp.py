from typing import TYPE_CHECKING

from django.conf import settings
from django.core.management.commands.startapp import Command as BaseCommand

if TYPE_CHECKING:
    from typing import Any


class Command(BaseCommand):
    def handle(self, **options: "Any") -> None:  # type: ignore[override]
        app_name = options["name"]

        directory = settings.BASE_DIR.parent / "apps" / app_name  # type: ignore[misc]
        directory.mkdir()
        directory = str(directory)

        if "template" not in options or options["template"] is None:
            template = str(settings.BASE_DIR.parent / ".django-app-template")  # type: ignore[misc]

        options.update(directory=directory, template=template)

        super().handle(**options)

        self.move_created_tests_directory(app_name=app_name)

    def move_created_tests_directory(self, app_name: str) -> None:
        root = settings.BASE_DIR.parent.parent  # type: ignore[misc]

        src = root / "src" / "apps" / app_name / "tests"
        dst = root / "tests" / "apps" / app_name

        dst.mkdir()
        src.rename(dst)
