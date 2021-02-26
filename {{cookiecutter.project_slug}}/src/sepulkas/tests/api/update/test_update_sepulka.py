import pytest

pytestmark = [pytest.mark.django_db]


def test_update_sepulka_instance(as_user, sepulka, new_image):
    as_user.put(f'/api/v1/sepulkas/{sepulka.id}/', {
        'title': 'The New Sepulka',
        'image': new_image,
    }, format='multipart')

    sepulka.refresh_from_db()
    assert sepulka.title == 'The New Sepulka'
    assert sepulka.image.name.endswith('.jpg')


def test_update_sepulka_response(as_user, sepulka, new_image):
    got = as_user.put(f'/api/v1/sepulkas/{sepulka.id}/', {
        'title': 'The New Sepulka',
        'image': new_image,
    }, format='multipart')

    assert got['title'] == 'The New Sepulka'
    assert got['image'].endswith('.jpg')
