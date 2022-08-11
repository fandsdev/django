import pytest

from pytest_mock import MockFixture

from django.db.transaction import atomic

from app.services import on_transaction_commit

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def dumb_function(mocker: MockFixture):
    return mocker.MagicMock()


@pytest.mark.parametrize('setting_value, called_times_in_transaction, called_times_after_transaction',
                         [
                             (True, 1, 1),
                             (False, 0, 1),
                         ])
def test_doesnt_call_before_commit(dumb_function, django_capture_on_commit_callbacks, settings, setting_value, called_times_in_transaction, called_times_after_transaction):
    wrapped = on_transaction_commit(dumb_function)  # noqa: AAA01

    with django_capture_on_commit_callbacks(execute=True), atomic():
        wrapped()
        assert dumb_function.call_count == called_times_in_transaction

    assert dumb_function.call_count == called_times_after_transaction
