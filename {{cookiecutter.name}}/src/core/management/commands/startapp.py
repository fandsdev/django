from typing import TYPE_CHECKING

from django.conf import settings
from django.core.management.commands.startapp import Command as BaseCommand

if TYPE_CHECKING:
    from argparse import ArgumentParser
    from typing import Any


class Command(BaseCommand):
    def add_arguments(self, parser: "ArgumentParser") -> None:
        super().add_arguments(parser)

        parser.add_argument(
            "--entity_name",
            help="The name of some application entity given in `snake_case`; e. g., if the application name is `users`, then the entity is `user`, and so on.",
        )

    def handle(self, **options: "Any") -> None:  # type: ignore[override]
        app_name = options["name"]

        directory = settings.BASE_DIR.parent / "apps" / app_name  # type: ignore[misc]
        directory.mkdir()
        directory = str(directory)

        if "template" not in options or options["template"] is None:
            template = str(settings.BASE_DIR.parent / ".django-app-template")  # type: ignore[misc]

        options.update(
            camel_case_entity_name=self.make_entity_name_camelized(options["entity_name"]),
            directory=directory,
            template=template,
        )

        super().handle(**options)

        self.rename_entity_name_modules(app_name=app_name, entity_name=options["entity_name"])
        self.add_app_to_installed_apps(app_name=app_name)
        self.move_created_tests_directory(app_name=app_name)

    def make_entity_name_camelized(self, entity_name: str) -> str:
        return entity_name.replace("_", " ").title().replace(" ", "")

    def rename_entity_name_modules(self, app_name: str, entity_name: str) -> None:
        app_dir = settings.BASE_DIR.parent / "apps" / app_name  # type: ignore[misc]

        for path in app_dir.rglob("*.py"):
            if "entity_name" in path.name:
                new_name = path.name.replace("entity_name", entity_name)
                path.rename(path.with_name(new_name))

    def add_app_to_installed_apps(self, app_name: str) -> None:
        installed_apps_path = settings.BASE_DIR / "conf" / "installed_apps.py"  # type: ignore[misc]

        with installed_apps_path.open() as reader:
            lines = reader.readlines()

            for lineno, line in enumerate(lines):
                if line.strip().startswith("APPS ="):
                    lines.insert(lineno + 1, f'    "apps.{app_name}",\n')
                    break

        with installed_apps_path.open("w") as writer:
            writer.writelines(lines)

    def move_created_tests_directory(self, app_name: str) -> None:
        root = settings.BASE_DIR.parent.parent  # type: ignore[misc]

        src = root / "src" / "apps" / app_name / "tests"
        dst = root / "tests" / "apps" / app_name

        dst.mkdir()
        src.rename(dst)
