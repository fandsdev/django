from typing import Protocol

from mixer.backend.django import mixer


class FactoryProtocol(Protocol):
    mixer: mixer


__all__ = [
    'FactoryProtocol',
]
