import pytest

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, user):
    got = as_user.get('/api/v1/users/me/')

    assert got['id'] == user.pk
    assert got['username'] == user.username


def test_anon(as_anon):
    got = as_anon.get('/api/v1/users/me/', as_response=True)

    assert got.status_code == 401
