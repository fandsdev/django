from django.core.files.uploadedfile import SimpleUploadedFile

from app.testing import register
from app.testing.types import FactoryProtocol


@register
def image(self: FactoryProtocol, name: str = "image.gif", content_type: str = "image/gif") -> SimpleUploadedFile:
    return SimpleUploadedFile(name=name, content=self.faker.image(), content_type=content_type)
