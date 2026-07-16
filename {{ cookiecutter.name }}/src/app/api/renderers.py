from collections.abc import Iterable, Mapping
from decimal import Decimal
from typing import Any
from uuid import UUID

import orjson
from django.utils.functional import Promise
from rest_framework.renderers import BaseRenderer

from app.api.case_converters import camelize_keys


def to_serializable(value: object) -> object:
    if isinstance(value, Promise | UUID | Decimal):
        return str(value)
    if isinstance(value, bytes | bytearray):
        raise TypeError(f"Type is not JSON serializable: {type(value).__name__}")
    if isinstance(value, Iterable):
        return camelize_keys(list(value))
    raise TypeError(f"Type is not JSON serializable: {type(value).__name__}")


class AppJSONRenderer(BaseRenderer):
    media_type = "application/json"
    format = "json"
    charset = "utf-8"  # force DRF to add charset to the content-type header

    def render(self, data: Any, accepted_media_type: str | None = None, renderer_context: Mapping[str, Any] | None = None) -> bytes:
        if data is None:
            return b""
        return orjson.dumps(camelize_keys(data), default=to_serializable)
