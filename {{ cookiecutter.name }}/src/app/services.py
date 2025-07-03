from abc import ABCMeta, abstractmethod
from collections.abc import Callable


class BaseService[T](metaclass=ABCMeta):
    """This is a template of a a base service.
    All services in the app should follow this rules:
      * Input variables should be done at the __init__ phase
      * Service should implement a single entrypoint without arguments

    This is ok:
      @dataclass
      class UserCreator(BaseService[User]):
        first_name: str
        last_name: str | None

        def act(self) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)

        # user = UserCreator(first_name="Ivan", last_name="Petrov")()

    This is not ok:
      class UserCreator:
        def __call__(self, first_name: str, last_name: str | None) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)

    For more implementation examples, check out https://github.com/tough-dev-school/education-backend/blob/master/src/apps/orders/services/order_course_changer.py
    """

    def __call__(self) -> T:
        self.validate()
        return self.act()

    def get_validators(self) -> list[Callable]:
        return []

    def validate(self) -> None:
        validators = self.get_validators()
        for validator in validators:
            validator()

    @abstractmethod
    def act(self) -> T: ...
