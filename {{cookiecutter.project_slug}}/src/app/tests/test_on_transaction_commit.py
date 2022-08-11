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


@pytest.fixture
def _on_commit_always_eager_false(settings):
    settings.ON_COMMIT_ALWAYS_EAGER = False


@pytest.fixture
def _on_commit_always_eager_true(settings):
    settings.ON_COMMIT_ALWAYS_EAGER = True


@pytest.mark.usefixtures('_on_commit_always_eager_false')   # noqa: AAA01
def test_doesnt_call_before_commit(dumb_function, django_capture_on_commit_callbacks):
    wrapped = on_transaction_commit(dumb_function)  # noqa: AAA01

    with django_capture_on_commit_callbacks(execute=True), atomic():
        wrapped()
        dumb_function.assert_not_called()

    dumb_function.assert_called_once()


@pytest.mark.usefixtures('_on_commit_always_eager_true')  # noqa: AAA01
def test_calls_if_flag_enabled(dumb_function, django_capture_on_commit_callbacks):
    wrapped = on_transaction_commit(dumb_function)   # noqa: AAA01

    with django_capture_on_commit_callbacks(execute=True), atomic():
        wrapped()
        dumb_function.assert_called_once()

    dumb_function.assert_called_once()
