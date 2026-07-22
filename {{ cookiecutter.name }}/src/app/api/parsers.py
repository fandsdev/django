from collections.abc import Mapping
from typing import IO, Any

import orjson
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser, DataAndFiles, FormParser, MultiPartParser

from app.api.case_converters import snakeize_keys, snakeize_query_dict


class AppJSONParser(BaseParser):
    media_type = "application/json"

    def parse(self, stream: IO[Any], media_type: str | None = None, parser_context: Mapping[str, Any] | None = None) -> Any:
        try:
            return snakeize_keys(orjson.loads(stream.read()))
        except orjson.JSONDecodeError as exc:
            raise ParseError(f"JSON parse error - {exc}") from exc


class AppFormParser(FormParser):
    def parse(self, stream: IO[Any], media_type: str | None = None, parser_context: Mapping[str, Any] | None = None) -> Any:
        return snakeize_query_dict(super().parse(stream, media_type, parser_context))


class AppMultiPartParser(MultiPartParser):
    def parse(self, stream: IO[Any], media_type: str | None = None, parser_context: Mapping[str, Any] | None = None) -> DataAndFiles:
        result = super().parse(stream, media_type, parser_context)
        return DataAndFiles(snakeize_query_dict(result.data), snakeize_query_dict(result.files))
