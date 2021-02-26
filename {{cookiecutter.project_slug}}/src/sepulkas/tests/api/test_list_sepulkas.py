import pytest

pytestmark = [pytest.mark.django_db]


def test_list_sepulkas(as_anon, sepulka):
    got = as_anon.get('/api/v1/sepulkas/')

    assert got['results'][0]['title'] == 'The Sepulka'
    assert got['results'][0]['image'].endswith('.jpg')
