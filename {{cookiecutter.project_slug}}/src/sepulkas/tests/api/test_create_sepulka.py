import pytest

from sepulkas.models import Sepulka

pytestmark = [pytest.mark.django_db]


def test_create_sepulka_instance(as_user, uploaded_image):
    as_user.post('/api/v1/sepulkas/', {
        'title': 'The Sepulka',
        'coverImage': uploaded_image,
    }, format='multipart')

    sepulka = Sepulka.objects.last()
    assert sepulka.title == 'The Sepulka'
    assert sepulka.cover_image.name.endswith('.gif')


def test_create_sepulka_response(as_user, uploaded_image):
    got = as_user.post('/api/v1/sepulkas/', {
        'title': 'The Sepulka',
        'coverImage': uploaded_image,
    }, format='multipart')

    assert got['title'] == 'The Sepulka'
    assert got['coverImage'].endswith('.gif')
