import pytest
from django.db import OperationalError


pytestmark = [
    pytest.mark.django_db,
]


def test(as_anon):
    result = as_anon.get("/api/v1/healthchecks/")

    assert result == {"db": True}


def test_503_when_database_is_down(as_anon, mocker):
    mocker.patch("django.db.connection.cursor", side_effect=OperationalError)  # connection.close() is a no-op on in-memory SQLite

    result = as_anon.get("/api/v1/healthchecks/", expected_status=503)

    assert result == {"db": False}
