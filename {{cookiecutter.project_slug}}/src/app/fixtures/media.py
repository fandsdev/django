from pathlib import Path
import pytest
import shutil
import tempfile
from typing import Generator

from django.conf import settings


@pytest.fixture(scope='session', autouse=True)
def _temporary_media() -> Generator[None, None, None]:
    settings.MEDIA_ROOT = Path(tempfile.gettempdir(), 'app/testmedia')
    Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
