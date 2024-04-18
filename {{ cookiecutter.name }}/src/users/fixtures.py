from typing import TYPE_CHECKING

import pytest

from users.models import User

if TYPE_CHECKING:
    from app.testing.factory import FixtureFactory


@pytest.fixture
def user(factory: "FixtureFactory") -> User:
    return factory.user()
