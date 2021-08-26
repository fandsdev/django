import pytest

pytestmark = [pytest.mark.django_db]


def test_list_sepulkas(as_anon, sepulka):
    got = as_anon.get('/api/v1/sepulkas/')

    assert got['results'][0]['title'] == 'The Sepulka'
    assert got['results'][0]['coverImage'].endswith('.gif')


def test_sepulkas_count(as_anon, factory):
    factory.cycle(10).sepulka()

    got = as_anon.get('/api/v1/sepulkas/')

    assert got['count'] == 10
