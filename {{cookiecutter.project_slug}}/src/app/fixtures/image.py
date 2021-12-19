import pytest
from typing import TYPE_CHECKING

from django.core.files.uploadedfile import SimpleUploadedFile

if TYPE_CHECKING:
    from app.testing.factory import FixtureFactory


@pytest.fixture
def uploaded_image(factory: 'FixtureFactory') -> SimpleUploadedFile:
    return factory.uploaded_image()
