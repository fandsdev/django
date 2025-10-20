from types import ModuleType
from typing import Protocol

from faker import Faker


class FactoryProtocol(Protocol):
    baker: ModuleType
    faker: Faker


__all__ = [
    "FactoryProtocol",
]
