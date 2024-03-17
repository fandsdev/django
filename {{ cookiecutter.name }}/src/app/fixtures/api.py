import pytest

from app.testing import ApiClient
from users.models import User


@pytest.fixture
def as_anon() -> ApiClient:
    return ApiClient()


@pytest.fixture
def as_user(user: User) -> ApiClient:
    return ApiClient(user=user)
