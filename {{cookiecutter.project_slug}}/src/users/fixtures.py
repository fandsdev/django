import pytest


@pytest.fixture
def anon(factory):
    return factory.anon()


@pytest.fixture
def user(factory):
    return factory.user()


@pytest.fixture
def staff(factory):
    return factory.user(is_staff=True)
