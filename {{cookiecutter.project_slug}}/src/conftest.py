import json
from datetime import datetime as stock_datetime
from unittest.mock import MagicMock

import pytest
import pytz
from django.utils import timezone
from mixer.backend.django import mixer as _mixer

from app.test.api_client import DRFClient


@pytest.fixture
def api():
    return DRFClient()


@pytest.fixture
def anon():
    return DRFClient(anon=True)


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user(mixer):
    return mixer.blend('users.User')


@pytest.fixture
def read_fixture():
    """JSON fixture reader"""

    def read_file(filename):
        with open(f'{filename}.json') as fp:
            return json.load(fp)

    return read_file


@pytest.fixture
def connect_mock_handler():
    def _connect_mock_handler(signal, **kwargs):
        handler = MagicMock()
        signal.connect(handler, **kwargs)
        return handler

    return _connect_mock_handler


@pytest.fixture
def datetime(settings):
    """Create a timezoned datetime"""
    def _f(*args, **kwargs):
        if isinstance(args[0], int):
            tz = settings.TIME_ZONE
        else:
            tz = args[0]
            args = args[1:]

        tz = pytz.timezone(tz)
        return timezone.make_aware(
            stock_datetime(*args, **kwargs),
            timezone=tz,
        )

    return _f
