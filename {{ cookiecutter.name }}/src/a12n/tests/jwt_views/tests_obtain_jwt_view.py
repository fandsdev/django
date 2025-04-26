import pytest
from axes.models import AccessAttempt
from freezegun import freeze_time


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("user"),
]


@pytest.fixture(autouse=True)
def _enable_django_axes(settings):
    settings.AXES_ENABLED = True


@pytest.fixture
def get_tokens(as_anon):
    def _get_tokens(username, password, expected_status=200):
        return as_anon.post(
            "/api/v1/auth/token/",
            {
                "username": username,
                "password": password,
            },
            expected_status=expected_status,
        )

    return _get_tokens


def test_get_token_pair(get_tokens):
    result = get_tokens("jwt-tester-user", "sn00pd0g")

    assert len(result["access"]) > 40
    assert len(result["refresh"]) > 40


def test_error_if_incorrect_password(get_tokens):
    result = get_tokens("jwt-tester-user", "50cent", expected_status=401)

    assert "Invalid username or password" in result["detail"]


def test_error_if_user_is_not_active(get_tokens, user):
    user.is_active = False
    user.save()

    result = get_tokens("jwt-tester-user", "sn00pd0g", expected_status=401)

    assert "Invalid username or password" in result["detail"]


def test_getting_token_with_incorrect_password_creates_access_attempt_log_entry(get_tokens):
    get_tokens("jwt-tester-user", "50cent", expected_status=401)

    assert AccessAttempt.objects.count() == 1


def test_access_token_gives_access_to_correct_user(get_tokens, as_anon, user):
    access_token = get_tokens("jwt-tester-user", "sn00pd0g")["access"]

    as_anon.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    result = as_anon.get("/api/v1/users/me/")

    assert result["id"] == user.id


@pytest.mark.freeze_time("2049-01-05 10:00:00Z")
def test_token_is_not_allowed_to_access_if_expired(as_anon, get_tokens):
    access_token = get_tokens("jwt-tester-user", "sn00pd0g")["access"]

    with freeze_time("2049-01-05 10:15:01Z"):
        as_anon.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        result = as_anon.get("/api/v1/users/me/", expected_status=401)

    assert "not valid" in result["detail"]
