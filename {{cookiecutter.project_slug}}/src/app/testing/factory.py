from functools import partial
from typing import Callable

from app.testing.mixer import mixer


def register(method: Callable) -> Callable:
    name = method.__name__
    FixtureRegistry.METHODS[name] = method
    return method


class FixtureRegistry:
    METHODS: dict[str, Callable] = {}

    def get(self, name: str) -> Callable:
        method = self.METHODS.get(name)
        if not method:
            raise AttributeError(f'Factory method “{name}” not found.')
        return method


class CycleFixtureFactory:
    def __init__(self, factory: 'FixtureFactory', count: int) -> None:
        self.factory = factory
        self.count = count

    def __getattr__(self, name: str) -> Callable:
        return lambda *args, **kwargs: [getattr(self.factory, name)(*args, **kwargs) for _ in range(self.count)]


class FixtureFactory:
    def __init__(self) -> None:
        self.mixer = mixer
        self.registry = FixtureRegistry()

    def __getattr__(self, name: str) -> Callable:
        method = self.registry.get(name)
        return partial(method, self)

    def cycle(self, count: int) -> CycleFixtureFactory:
        """
        Run given method X times:
            factory.cycle(5).order()  # gives 5 orders
        """
        return CycleFixtureFactory(self, count)
