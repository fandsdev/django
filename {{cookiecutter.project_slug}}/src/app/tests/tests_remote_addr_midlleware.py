import pytest

from django.apps import apps

from app.test.api_client import DRFClient

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def _require_users_app_installed(settings):
    assert apps.is_installed('users'), """
        Stock f213/django users app should be installed to run this test.

        Make sure to test app.middleware.real_ip.real_ip_middleware on your own, if you drop
        the stock users app.
    """


@pytest.fixture
def api():
    return DRFClient(HTTP_X_FORWARDED_FOR='100.200.250.150, 10.0.0.1')


def test(api):
    got = api.get('/api/v1/users/me/')

    assert got['remoteAddr'] == '100.200.250.150'
