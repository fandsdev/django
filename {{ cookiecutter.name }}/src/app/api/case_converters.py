"""Conversion between Python snake_case and wire camelCase API keys.

Policy:
- Python keys are words of [a-z0-9] joined by single underscores, wire keys are lowerCamelCase.
- A digit belongs to the preceding word: field2_name <-> field2Name.

Round-trip is guaranteed only for keys that follow this convention;
keys with double or leading underscores, capitalized abbreviations or digit-only words are out of scope.
"""

import re

from django.http import QueryDict
from django.utils.datastructures import MultiValueDict


camel_boundary_re = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def snake_to_camel(key: str) -> str:
    first, *rest = key.split("_")
    return first + "".join(word.capitalize() for word in rest)


def camel_to_snake(key: str) -> str:
    return camel_boundary_re.sub("_", key).lower()


def camelize_keys(data: object) -> object:
    if isinstance(data, dict):
        return {snake_to_camel(key) if isinstance(key, str) else key: camelize_keys(value) for key, value in data.items()}
    if isinstance(data, list | tuple):
        return [camelize_keys(item) for item in data]
    return data


def snakeize_keys(data: object) -> object:
    if isinstance(data, dict):
        return {camel_to_snake(key) if isinstance(key, str) else key: snakeize_keys(value) for key, value in data.items()}
    if isinstance(data, list | tuple):
        return [snakeize_keys(item) for item in data]
    return data


def snakeize_query_dict(data: MultiValueDict) -> MultiValueDict:
    result = QueryDict(mutable=True) if isinstance(data, QueryDict) else MultiValueDict()
    for key in data:
        result.setlist(camel_to_snake(key), data.getlist(key))
    return result
