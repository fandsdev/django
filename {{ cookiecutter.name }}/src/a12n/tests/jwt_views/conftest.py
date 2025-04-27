import pytest
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user(factory):
    user = factory.user(username="jwt-tester-user")
    user.set_password("sn00pd0g")
    user.save()

    return user


@pytest.fixture
def initial_token_pair(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@pytest.fixture
def refresh_tokens(as_anon):
    def _refresh_tokens(token, expected_status=200):
        return as_anon.post(
            "/api/v1/auth/token/refresh/",
            {
                "refresh": token,
            },
            expected_status=expected_status,
        )

    return _refresh_tokens
