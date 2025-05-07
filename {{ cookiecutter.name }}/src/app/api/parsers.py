from typing import IO, Any

from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import underscoreize
from drf_orjson_renderer.parsers import ORJSONParser
from rest_framework.exceptions import ParseError


class AppJSONParser(ORJSONParser):
    """Combination of ORJSONParser and CamelCaseJSONParser"""

    # djangorestframework_camel_case parameter
    # details: https://github.com/vbabiy/djangorestframework-camel-case?tab=readme-ov-file#underscoreize-options
    json_underscoreize = api_settings.JSON_UNDERSCOREIZE

    def parse(self, stream: IO[Any], media_type: Any = None, parser_context: Any = None) -> Any:
        try:
            data = super().parse(stream, media_type, parser_context)
            return underscoreize(data, **self.json_underscoreize)
        except ValueError as exc:
            raise ParseError(f"JSON parse error - {exc}")
