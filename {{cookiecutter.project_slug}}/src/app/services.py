from abc import ABCMeta
from abc import abstractmethod
from functools import wraps
from typing import Callable

from django.conf import settings
from django.db import transaction


class BaseService(metaclass=ABCMeta):
    """This is a template of a base service.
    All services in the app should follow this rules:
      * Input variables should be done at the __init__ phase
      * Service should implement a single entrypoint without arguments

    This is ok:
      @dataclass
      class UserCreator(BaseService):
        first_name: str
        last_name: Optional[str]

        def act(self) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)

    user = UserCreator(first_name='Ivan', last_name='Petrov')()

    This is not ok:
      class UserCreator:
        def __call__(self, first_name: str, last_name: Optional[str]) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)

    For more implementation examples, check out https://github.com/tough-dev-school/education-backend/tree/master/src/orders/services
    """
    def __call__(self) -> None:
        self.validate()
        return self.act()

    def get_validators(self) -> list[Callable]:
        return []

    def validate(self) -> None:
        validators = self.get_validators()
        for validator in validators:
            validator()

    @abstractmethod
    def act(self) -> None:
        raise NotImplementedError('Please implement in the service class')


def on_transaction_commit(fn: Callable) -> Callable:
    """
    Creates callback that will be executed when current transaction
    will be successfully committed.

    Helps when you need to start a celery task after some object creation
    in transaction.

    https://github.com/fandsdev/django/issues/519#issuecomment-1205180739

    Usage example:

    @dataclass
    class UserCreator(BaseService):
        first_name: str
        last_name: Optional[str]
        avatar: Optional[str]

        def act(self) -> User:
            user = User.objects.create(first_name=self.first_name, last_name=self.last_name)
            self.download_user_avatar(user.id)
            return

        @on_transaction_commit
        def download_user_avatar(self, user_id):
            download_user_avatar_celery_task.delay(user_id)
    """

    @wraps(fn)
    def wrapped(*args, **kwargs) -> None:  # type: ignore
        if settings.ON_COMMIT_ALWAYS_EAGER:
            fn(*args, **kwargs)
        else:
            transaction.on_commit(lambda: fn(*args, **kwargs))

    return wrapped
