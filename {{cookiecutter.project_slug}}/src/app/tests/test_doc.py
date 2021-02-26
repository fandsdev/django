import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_html(api):
    got = api.get('/api/v1/docs/')

    assert '/static/drf-yasg/redoc-init' in got


def test_json(api):
    got = api.get('/api/v1/swagger.json')

    assert 'basePath' in got


def test_yaml(api):
    got = api.get('/api/v1/swagger.yaml')

    assert 'basePath:' in got
