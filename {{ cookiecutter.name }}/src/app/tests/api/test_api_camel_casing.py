import io
import json
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlencode
from uuid import UUID

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import gettext_lazy
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from app.api.parsers import AppFormParser, AppJSONParser, AppMultiPartParser
from app.api.renderers import AppJSONRenderer
from app.api.spectacular import camelize_serializer_fields


pytestmark = [
    pytest.mark.django_db,
]


def test_renderer_camelizes_keys():
    rendered = AppJSONRenderer().render({"first_name": "Ann", "home_address": {"zip_code": "12345"}, "field2_name": "Ann"})

    assert json.loads(rendered) == {"firstName": "Ann", "homeAddress": {"zipCode": "12345"}, "field2Name": "Ann"}


def test_renderer_returns_empty_bytes_for_none():
    assert AppJSONRenderer().render(None) == b""


def test_renderer_serializes_django_types():
    data = {
        "id": UUID("0195b1e0-6f0e-7000-8000-000000000000"),
        "price": Decimal("9.90"),
        "created": datetime(2026, 1, 2, 3, 4, 5),
        "label": gettext_lazy("Lazy Text"),
        "letters": (letter for letter in "ab"),
    }

    rendered = json.loads(AppJSONRenderer().render(data))

    assert rendered == {
        "id": "0195b1e0-6f0e-7000-8000-000000000000",
        "price": "9.90",
        "created": "2026-01-02T03:04:05",
        "label": "Lazy Text",
        "letters": ["a", "b"],
    }


def test_renderer_rejects_unknown_types():
    with pytest.raises(TypeError):
        AppJSONRenderer().render({"value": object()})


def test_renderer_camelizes_keys_inside_lazy_iterables():
    data = {"items": ({"tag_name": str(index)} for index in range(2))}

    rendered = json.loads(AppJSONRenderer().render(data))

    assert rendered == {"items": [{"tagName": "0"}, {"tagName": "1"}]}


def test_renderer_rejects_bytes():
    with pytest.raises(TypeError):
        AppJSONRenderer().render({"value": b"raw"})


def test_json_parser_snakeizes_keys():
    parsed = AppJSONParser().parse(io.BytesIO(b'{"firstName":"Ann","homeAddress":{"zipCode":"12345"},"field2Name":"Ann"}'))

    assert parsed == {"first_name": "Ann", "home_address": {"zip_code": "12345"}, "field2_name": "Ann"}


def test_json_parser_rejects_invalid_json():
    with pytest.raises(ParseError):
        AppJSONParser().parse(io.BytesIO(b"{broken"))


def test_json_parser_rejects_non_utf8_body():
    with pytest.raises(ParseError):
        AppJSONParser().parse(io.BytesIO(b'{"a":"\xff"}'))


def test_form_parser_snakeizes_keys():
    request = APIRequestFactory().post("/", urlencode({"firstName": "Ann"}), content_type="application/x-www-form-urlencoded")

    data = Request(request, parsers=[AppFormParser()]).data

    assert data["first_name"] == "Ann"


def test_multipart_parser_snakeizes_data_and_file_keys():
    upload = SimpleUploadedFile("avatar.png", b"image-bytes", content_type="image/png")
    request = APIRequestFactory().post("/", {"firstName": "Ann", "avatarFile": upload}, format="multipart")

    data = Request(request, parsers=[AppMultiPartParser()]).data

    assert data["first_name"] == "Ann"
    assert data["avatar_file"].name == "avatar.png"


def test_schema_camel_casing(as_anon):
    response = as_anon.get("/api/v1/docs/schema/", as_response=True)

    content = response.content.decode()

    assert "User:" in content
    assert "firstName:" in content
    assert "remoteAddr:" in content


def test_spectacular_camelize_serializer_fields():
    result = {
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "home_address": {
                            "type": "object",
                            "properties": {"zip_code": {"type": "string"}},
                            "required": ["zip_code"],
                        },
                    },
                    "required": ["first_name"],
                }
            }
        }
    }

    camelized = camelize_serializer_fields(result, generator=None)

    assert camelized["components"]["schemas"]["User"]["properties"]["firstName"] == {"type": "string"}
    assert camelized["components"]["schemas"]["User"]["properties"]["homeAddress"]["properties"]["zipCode"] == {"type": "string"}
    assert camelized["components"]["schemas"]["User"]["properties"]["homeAddress"]["required"] == ["zipCode"]
    assert camelized["components"]["schemas"]["User"]["required"] == ["firstName"]


def test_spectacular_camelize_schema_variants():
    result = {
        "components": {
            "schemas": {
                "Payload": {
                    "type": "object",
                    "properties": {
                        "entries": {"type": "array", "items": {"type": "object", "properties": {"zip_code": {"type": "string"}}}},
                        "extras": {"type": "object", "additionalProperties": {"type": "object", "properties": {"street_name": {"type": "string"}}}},
                    },
                    "allOf": [{"type": "object", "properties": {"first_name": {"type": "string"}}}],
                    "anyOf": [{"type": "object", "properties": {"last_name": {"type": "string"}}}],
                    "oneOf": [{"type": "object", "properties": {"middle_name": {"type": "string"}}}],
                }
            }
        }
    }

    camelized = camelize_serializer_fields(result, generator=None)

    schema = camelized["components"]["schemas"]["Payload"]
    assert schema["properties"]["entries"]["items"]["properties"] == {"zipCode": {"type": "string"}}
    assert schema["properties"]["extras"]["additionalProperties"]["properties"] == {"streetName": {"type": "string"}}
    assert schema["allOf"] == [{"type": "object", "properties": {"firstName": {"type": "string"}}}]
    assert schema["anyOf"] == [{"type": "object", "properties": {"lastName": {"type": "string"}}}]
    assert schema["oneOf"] == [{"type": "object", "properties": {"middleName": {"type": "string"}}}]
