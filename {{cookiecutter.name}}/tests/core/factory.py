from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker

from core.testing import register
from core.testing.types import FactoryProtocol

faker = Faker()


@register
def image(self: FactoryProtocol, name: str = "image.gif", content_type: str = "image/gif") -> SimpleUploadedFile:
    return SimpleUploadedFile(name=name, content=faker.image(), content_type=content_type)
