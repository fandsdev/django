import pytest

from app.testing.factory import FixtureFactory


@pytest.fixture
def factory() -> FixtureFactory:
    return FixtureFactory()
