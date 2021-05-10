import pytest

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.filterwarnings('ignore:.*inspect.getargspec().*:DeprecationWarning'),
]


def test(as_anon):
    got = as_anon.get('/api/v1/healthchecks/db/')

    assert got == 'true'
