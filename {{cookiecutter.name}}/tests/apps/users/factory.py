from django.contrib.auth.models import AnonymousUser

from apps.users.models import User
from core.testing import register
from core.testing.types import FactoryProtocol


@register
def user(self: FactoryProtocol, **kwargs: dict) -> User:
    return self.mixer.blend("users.User", **kwargs)


@register
def anon(self: FactoryProtocol, **kwargs: dict) -> AnonymousUser:
    return AnonymousUser()