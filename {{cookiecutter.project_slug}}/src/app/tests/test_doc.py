import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_html(as_anon):
    result = as_anon.get('/api/v1/docs/')

    assert '/static/drf-yasg/redoc-init' in result


def test_json(as_anon):
    result = as_anon.get('/api/v1/swagger.json')

    assert 'basePath' in result


def test_yaml(as_anon):
    result = as_anon.get('/api/v1/swagger.yaml')

    assert 'basePath:' in result
