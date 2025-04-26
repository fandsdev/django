import pytest
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("user"),
]


@pytest.fixture
def logout(as_anon):
    def _logout(token, expected_status=200):
        return as_anon.post(
            "/api/v1/auth/logout/",
            {
                "refresh": token,
            },
            expected_status=expected_status,
        )

    return _logout


def test_logout_token_saved_to_blacklist(logout, initial_token_pair):
    logout(initial_token_pair["refresh"])

    assert BlacklistedToken.objects.get(token__token=initial_token_pair["refresh"])


def test_logout_refresh_token_impossible_to_reuse(initial_token_pair, logout, as_anon):
    logout(initial_token_pair["refresh"])

    result = as_anon.post(
        path="/api/v1/auth/token/refresh/",
        data={"refresh": initial_token_pair["refresh"]},
        expected_status=401,
    )

    assert "blacklisted" in result["detail"]
