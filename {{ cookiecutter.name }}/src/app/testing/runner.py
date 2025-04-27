from typing import Any

from django.core.management.base import CommandError


class DisableTestCommandRunner:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def run_tests(self, *args: Any) -> None:
        raise CommandError("Pytest here. Run it with `make test`")
