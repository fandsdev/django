from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager


class User(AbstractUser):  # noqa
    objects: ClassVar[_UserManager] = _UserManager()
