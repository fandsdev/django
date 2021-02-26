import pytest

from sepulkas.models import Sepulka

pytestmark = [pytest.mark.django_db]


def test_create_sepulka_instance(as_user, uploaded_image):
    as_user.post('/api/v1/sepulkas/', {
        'title': 'The Sepulka',
        'image': uploaded_image,
    }, format='multipart')

    sepulka = Sepulka.objects.last()
    assert sepulka.title == 'The Sepulka'
    assert sepulka.image.name.endswith('.jpg')


def test_create_sepulka_response(as_user, uploaded_image):
    got = as_user.post('/api/v1/sepulkas/', {
        'title': 'The Sepulka',
        'image': uploaded_image,
    }, format='multipart')

    assert got['title'] == 'The Sepulka'
    assert got['image'].endswith('.jpg')
