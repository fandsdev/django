import pytest

from freezegun import freeze_time

from a12n.utils import get_jwt

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time('2049-01-05'),
]


@pytest.fixture
def refresh_token(as_user):
    def _refresh_token(token, expected_status=201):
        return as_user.post('/api/v1/auth/token/refresh/', {
            'token': token,
        }, format='json', expected_status=expected_status)

    return _refresh_token


@pytest.fixture
def initial_token(as_user):
    with freeze_time('2049-01-03'):
        return get_jwt(as_user.user)


def test_refresh_token_ok(initial_token, refresh_token):
    result = refresh_token(initial_token)

    assert 'token' in result


def test_refreshed_token_is_a_token(initial_token, refresh_token):
    result = refresh_token(initial_token)

    assert len(result['token']) > 32


def test_refreshed_token_is_new_one(initial_token, refresh_token):
    result = refresh_token(initial_token)

    assert result['token'] != initial_token


def test_refresh_token_fails_with_incorrect_previous_token(refresh_token):
    result = refresh_token('some-invalid-previous-token', expected_status=400)

    assert 'nonFieldErrors' in result


def test_token_is_not_allowed_to_refresh_if_expired(initial_token, refresh_token):
    with freeze_time('2049-02-05'):

        result = refresh_token(initial_token, expected_status=400)

    assert 'expired' in result['nonFieldErrors'][0]


def test_received_token_works(as_anon, refresh_token, initial_token):
    token = refresh_token(initial_token)['token']
    as_anon.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    result = as_anon.get('/api/v1/users/me/')

    assert result is not None
