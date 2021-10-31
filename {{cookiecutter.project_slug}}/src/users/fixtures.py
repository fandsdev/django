import pytest


@pytest.fixture
def user(factory):
    return factory.user()
