import pytest
from freezegun import freeze_time


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("user"),
]


def test_refresh_token_endpoint_token_pair(initial_token_pair, refresh_tokens):
    refreshed_token_pair = refresh_tokens(initial_token_pair["refresh"])

    assert len(refreshed_token_pair["access"]) > 40
    assert len(refreshed_token_pair["refresh"]) > 40


def test_refresh_tokens_are_new(initial_token_pair, refresh_tokens):
    refreshed_token_pair = refresh_tokens(initial_token_pair["refresh"])

    assert initial_token_pair["access"] != refreshed_token_pair["access"]
    assert initial_token_pair["refresh"] != refreshed_token_pair["refresh"]


def test_refreshed_access_token_works_as_expected(initial_token_pair, refresh_tokens, user, as_anon):
    refreshed_access_token = refresh_tokens(initial_token_pair["refresh"])["access"]

    as_anon.credentials(HTTP_AUTHORIZATION=f"Bearer {refreshed_access_token}")
    result = as_anon.get("/api/v1/users/me/")

    assert result["id"] == user.id


def test_refreshed_refresh_token_is_also_good(initial_token_pair, refresh_tokens, user, as_anon):
    refreshed_refresh_token = refresh_tokens(initial_token_pair["refresh"])["refresh"]
    last_refreshed_access_token = refresh_tokens(refreshed_refresh_token)["access"]

    as_anon.credentials(HTTP_AUTHORIZATION=f"Bearer {last_refreshed_access_token}")
    result = as_anon.get("/api/v1/users/me/")

    assert result["id"] == user.id


def test_refresh_token_fails_if_user_is_not_active(refresh_tokens, initial_token_pair, user):
    user.is_active = False
    user.save()

    result = refresh_tokens(initial_token_pair["refresh"], expected_status=401)

    assert "No active account found" in result["detail"]


def test_refresh_token_fails_with_incorrect_previous_token(refresh_tokens):
    result = refresh_tokens("some-invalid-previous-token", expected_status=401)

    assert "Token is invalid" in result["detail"]


@pytest.mark.freeze_time("2049-01-01 10:00:00Z")
def test_token_is_not_allowed_to_refresh_if_expired(initial_token_pair, refresh_tokens):
    with freeze_time("2049-01-22 10:00:01Z"):  # 21 days and 1 second later
        result = refresh_tokens(initial_token_pair["refresh"], expected_status=401)

    assert "expired" in result["detail"]


def test_token_is_not_allowed_to_refresh_twice(initial_token_pair, refresh_tokens):
    refresh_tokens(initial_token_pair["refresh"])

    result = refresh_tokens(initial_token_pair["refresh"], expected_status=401)

    assert "blacklisted" in result["detail"]
