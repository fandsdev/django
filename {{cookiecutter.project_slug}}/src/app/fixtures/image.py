import pytest


@pytest.fixture
def uploaded_image(factory):
    return factory.uploaded_image()
