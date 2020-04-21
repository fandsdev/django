from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager


class User(AbstractUser):
    objects = _UserManager()  # type: _UserManager
