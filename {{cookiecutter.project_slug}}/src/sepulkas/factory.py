from app.testing import register


@register
def sepulka(self, **kwargs):
    return self.mixer.blend('sepulkas.Sepulka', **kwargs)
