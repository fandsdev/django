import pytest

from sepulkas.models import Sepulka

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time('2002-02-02'),
]


def test_create_sepulka_instance(api):
    api.post('/api/v1/sepulkas/', {
        'name': 'Sepulka',
        'description': 'Check sepulkarium',
    })

    sepulka = Sepulka.objects.last()
    assert sepulka.name == 'Sepulka'
    assert sepulka.description == 'Check sepulkarium'


def test_create_sepulka_response_is_detail(api):
    got = api.post('/api/v1/sepulkas/', {
        'name': 'Sepulka',
        'description': 'Check sepulkarium',
    })

    assert got['name'] == 'Sepulka'
    assert got['description'] == 'Check sepulkarium'
    assert got['created'] == '2002-02-02T00:00:00Z'
    assert got['modified'] is None


def test_create_sepulka_with_create_serializer(api, datetime):
    api.post('/api/v1/sepulkas/', {
        'name': 'Sepulka',
        'description': 'Check sepulkarium',
        'created': '123',
        'modified': '123',
    })

    sepulka = Sepulka.objects.last()
    assert sepulka.name == 'Sepulka'
    assert sepulka.description == 'Check sepulkarium'
    assert sepulka.created == datetime(2002, 2, 2)
    assert sepulka.modified is None
