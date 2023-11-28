import pytest
from typing import TYPE_CHECKING

from core.testing import ApiClient
from core.testing.factory import FixtureFactory

if TYPE_CHECKING:
    from apps.users.models import User


@pytest.fixture
def as_anon() -> "ApiClient":
    return ApiClient()


@pytest.fixture
def as_user(user: "User") -> "ApiClient":
    return ApiClient(user=user)


@pytest.fixture
def factory() -> "FixtureFactory":
    return FixtureFactory()
