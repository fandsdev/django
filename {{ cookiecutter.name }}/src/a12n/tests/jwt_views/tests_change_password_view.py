import pytest
from rest_framework_simplejwt.tokens import RefreshToken


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("user"),
]


@pytest.fixture(autouse=True)
def enable_en_i18n(settings):
    """Enable English i18n for tests."""
    settings.LANGUAGE_CODE = "en"
    return settings


@pytest.fixture
def override_password_validators(settings):
    """Set two password validators for tests."""
    settings.AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]
    return settings


@pytest.fixture
def change_password(as_anon, initial_token_pair):
    def _change(old_password, new_password, expected_status=200):
        as_anon.credentials(HTTP_AUTHORIZATION=f"Bearer {initial_token_pair['access']}")

        return as_anon.post(
            "/api/v1/auth/password/change/",
            {
                "oldPassword": old_password,
                "newPassword": new_password,
            },
            expected_status=expected_status,
        )

    return _change


def test_password_actually_changed(change_password):
    result = change_password("sn00pd0g", "kiTTy")

    assert len(result["access"]) > 40
    assert len(result["refresh"]) > 40


def test_return_access_token_with_access_of_correct_user(change_password, as_anon, user):
    access_token = change_password("sn00pd0g", "kiTTy")["access"]

    as_anon.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    result = as_anon.get("/api/v1/users/me/")

    assert result["id"] == user.id


def test_changing_password_with_incorrect_old_password_fails(change_password):
    result = change_password("50cent", "kiTTy", expected_status=400)

    assert result["oldPassword"] == ["Your old password was entered incorrectly. Please enter it again."]


@pytest.mark.usefixtures("override_password_validators")
def test_changing_password_check_password_constraints(change_password):
    result = change_password("sn00pd0g", "12345", expected_status=400)

    assert "newPassword" in result
    assert result["newPassword"] == [
        "This password is too short. It must contain at least 10 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ]


def test_changing_password_blacklists_all_active_user_tokens(change_password, refresh_tokens, user):
    active_refresh_token = str(RefreshToken.for_user(user))
    change_password("sn00pd0g", "kiTTy")

    result = refresh_tokens(active_refresh_token, expected_status=401)

    assert "blacklisted" in result["detail"]


def test_change_password_anon_forbidden(as_anon):
    result = as_anon.post(
        "/api/v1/auth/password/change/",
        {
            "oldPassword": "sn00pd0g",
            "newPassword": "kiTTy",
        },
        as_response=True,
    )

    assert result.status_code == 401
