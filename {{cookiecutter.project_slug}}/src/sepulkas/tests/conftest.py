import pytest


@pytest.fixture
def sepulka(factory, uploaded_image):
    defaults = {
        'title': 'The Sepulka',
        'image': uploaded_image,
    }
    return factory.sepulka(**defaults)
