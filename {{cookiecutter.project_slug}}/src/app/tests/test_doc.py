import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_html(as_anon):
    got = as_anon.get('/api/v1/docs/')

    assert '/static/drf-yasg/redoc-init' in got


def test_json(as_anon):
    got = as_anon.get('/api/v1/swagger.json')

    assert 'basePath' in got


def test_yaml(as_anon):
    got = as_anon.get('/api/v1/swagger.yaml')

    assert 'basePath:' in got
