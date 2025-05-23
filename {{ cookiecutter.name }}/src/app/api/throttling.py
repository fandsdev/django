from typing import Protocol

from django.conf import settings
from rest_framework.request import Request
from rest_framework.views import APIView


class BaseThrottle(Protocol):
    def allow_request(self, request: Request, view: APIView) -> bool: ...


class ConfigurableThrottlingMixin:
    def allow_request(self: BaseThrottle, request: Request, view: APIView) -> bool:
        if settings.DISABLE_THROTTLING:
            return True

        return super().allow_request(request, view)  # type: ignore[safe-super]
