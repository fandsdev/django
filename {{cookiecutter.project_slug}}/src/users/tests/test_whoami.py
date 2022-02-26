import pytest

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, user):
    result = as_user.get('/api/v1/users/me/')

    assert result['id'] == user.pk
    assert result['username'] == user.username


def test_anon(as_anon):
    result = as_anon.get('/api/v1/users/me/', as_response=True)

    assert result.status_code == 401
