import pytest

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.filterwarnings('ignore:.*inspect.getargspec().*:DeprecationWarning'),
]


def test(api):
    got = api.get('/api/v1/healthchecks/db/')

    assert got == 'true'
