from typing import TYPE_CHECKING

import pytest

from apps.users.models import User

if TYPE_CHECKING:
    from core.testing.factory import FixtureFactory


@pytest.fixture
def user(factory: "FixtureFactory") -> User:
    return factory.user()
