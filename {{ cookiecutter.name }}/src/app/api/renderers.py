from typing import Any

from djangorestframework_camel_case.util import camelize
from drf_orjson_renderer.renderers import ORJSONRenderer


class AppJSONRenderer(ORJSONRenderer):
    """Combination of CamelCaseJSONRenderer and ORJSONRenderer"""

    charset = "utf-8"  # force DRF to add charset header to the content-type
    json_underscoreize = {"no_underscore_before_number": True}  # https://github.com/vbabiy/djangorestframework-camel-case#underscoreize-options

    def render(self, data: Any, *args: Any, **kwargs: Any) -> bytes:
        return super().render(camelize(data, **self.json_underscoreize), *args, **kwargs)
