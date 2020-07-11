import pytest

from sepulkas.models import Sepulka

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time('2002-02-02'),
]


def test_update_sepulka_instance(api, sepulka):
    api.patch(f'/api/v1/sepulkas/{sepulka.id}/', {
        'description': 'Check sepulation',
    })

    sepulka = Sepulka.objects.last()
    assert sepulka.description == 'Check sepulation'


def test_update_sepulka_with_update_serializer(api, sepulka):
    api.patch(f'/api/v1/sepulkas/{sepulka.id}/', {
        'name': 'Sepulkarium',
    })

    sepulka = Sepulka.objects.last()
    assert sepulka.name == 'Sepulka'  # Default serializer would have updated name here


def test_update_sepulka_response_is_detail(api, sepulka):
    got = api.patch(f'/api/v1/sepulkas/{sepulka.id}/', {
        'description': 'Check sepulation',
    })

    assert got['name'] == 'Sepulka'
    assert got['description'] == 'Check sepulation'
    assert got['created'] == '2002-02-02T00:00:00Z'
    assert got['modified'] == '2002-02-02T00:00:00Z'
