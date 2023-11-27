from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from typing import ClassVar


class User(AbstractUser):  # noqa
    objects: ClassVar[_UserManager] = _UserManager()
