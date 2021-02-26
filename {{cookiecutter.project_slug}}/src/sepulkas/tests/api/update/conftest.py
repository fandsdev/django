import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def new_image(factory):
    return factory.uploaded_image()
