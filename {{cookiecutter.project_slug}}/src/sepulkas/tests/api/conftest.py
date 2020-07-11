import pytest
from mixer.backend.django import mixer


@pytest.fixture
def sepulka_factory():
    def _create_sepulka(**kwargs):
        defaults = {'name': 'Sepulka', 'description': 'Check sepulkarium', **kwargs}
        return mixer.blend('sepulkas.Sepulka', **defaults)
    return _create_sepulka


@pytest.fixture
def sepulka(sepulka_factory):
    return sepulka_factory()
