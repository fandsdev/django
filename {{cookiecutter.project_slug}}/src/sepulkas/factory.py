from app.testing import register
from app.testing.types import FactoryProtocol
from sepulkas.models import Sepulka


@register
def sepulka(self: FactoryProtocol, **kwargs: dict) -> Sepulka:
    return self.mixer.blend('sepulkas.Sepulka', **kwargs)
