import json
import pytest

from axes.models import AccessAttempt

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _enable_django_axes(settings):
    settings.AXES_ENABLED = True


@pytest.fixture
def get_token(as_user):
    def _get_token(username, password, expected_status=201):
        return as_user.post('/api/v1/auth/token/', {
            'username': username,
            'password': password,
        }, format='json', expected_status=expected_status)

    return _get_token


def _decode(response):
    return json.loads(response.content.decode('utf-8', errors='ignore'))


def test_getting_token_ok(as_user, get_token):
    result = get_token(as_user.user.username, as_user.password)

    assert 'token' in result


def test_getting_token_is_token(as_user, get_token):
    result = get_token(as_user.user.username, as_user.password)

    assert len(result['token']) > 32  # every stuff that is long enough, may be a JWT token


def test_getting_token_with_incorrect_password(as_user, get_token):
    result = get_token(as_user.user.username, 'z3r0c00l', expected_status=400)

    assert 'nonFieldErrors' in result


def test_getting_token_with_incorrect_password_creates_access_attempt_log_entry(as_user, get_token):
    get_token(as_user.user.username, 'z3r0c00l', expected_status=400)  # act

    assert AccessAttempt.objects.count() == 1


@pytest.mark.parametrize(('extract_token', 'status_code'), [  # NOQA: AAA01
    (lambda response: response['token'], 200),
    (lambda *args: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRpbW90aHk5NSIsImlhdCI6MjQ5MzI0NDgwMCwiZXhwIjoyNDkzMjQ1MTAwLCJqdGkiOiI2MWQ2MTE3YS1iZWNlLTQ5YWEtYWViYi1mOGI4MzBhZDBlNzgiLCJ1c2VyX2lkIjoxLCJvcmlnX2lhdCI6MjQ5MzI0NDgwMH0.YQnk0vSshNQRTAuq1ilddc9g3CZ0s9B0PQEIk5pWa9I', 401),
    (lambda *args: 'sh1t', 401),
])
def test_received_token_works(as_user, get_token, as_anon, extract_token, status_code):
    token = extract_token(get_token(as_user.user.username, as_user.password))

    as_anon.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    as_anon.get('/api/v1/users/me/', expected_status=status_code)
