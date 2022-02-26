import pytest

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.filterwarnings('ignore:.*inspect.getargspec().*:DeprecationWarning'),
]


def test(as_anon):
    result = as_anon.get('/api/v1/healthchecks/db/')

    assert result == 'true'
