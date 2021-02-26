import pytest

pytestmark = [pytest.mark.django_db]


def test_retrieve_sepulka(as_anon, sepulka):
    got = as_anon.get(f'/api/v1/sepulkas/{sepulka.id}/')

    assert got['title'] == 'The Sepulka'
    assert got['image'].endswith('.jpg')
