import pytest
from unittest.mock import call
from unittest.mock import Mock

from app.testing import FixtureFactory
from app.testing import register


@pytest.fixture
def fixture_factory() -> FixtureFactory:
    return FixtureFactory()


@pytest.fixture
def registered_method() -> Mock:
    mock = Mock(name='registered_method', return_value='i should be returned after gettatr')
    mock.__name__ = 'registered_method'
    register(mock)
    return mock


def test_call_getattr_returns_what_method_returned(fixture_factory: FixtureFactory, registered_method: Mock):
    got = fixture_factory.registered_method()

    assert got == 'i should be returned after gettatr'


def test_registered_method_called_with_factory_instance(fixture_factory: FixtureFactory, registered_method: Mock):
    fixture_factory.registered_method(foo=1)

    registered_method.assert_called_with(fixture_factory, foo=1)


def test_cycle_returns_given_method_n_times(fixture_factory: FixtureFactory, registered_method: Mock):
    fixture_factory.cycle(4).registered_method(bar=1)

    registered_method.assert_has_calls(
        calls=[
            call(fixture_factory, bar=1),
            call(fixture_factory, bar=1),
            call(fixture_factory, bar=1),
            call(fixture_factory, bar=1),
        ],
    )
