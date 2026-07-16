from typing import Any

from app.api.case_converters import snake_to_camel


def camelize_serializer_fields(result: dict[str, Any], generator: Any, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG001
    for schema in result.get("components", {}).get("schemas", {}).values():
        camelize_schema(schema)
    return result


def camelize_schema_properties(schema: dict[str, Any]) -> dict[str, Any]:
    if isinstance(schema.get("properties"), dict):
        schema["properties"] = {snake_to_camel(name): camelize_schema(prop) for name, prop in schema["properties"].items()}
    if isinstance(schema.get("required"), list):
        schema["required"] = [snake_to_camel(name) for name in schema["required"]]
    for keyword in ("items", "additionalProperties"):
        if isinstance(schema.get(keyword), dict):
            schema[keyword] = camelize_schema(schema[keyword])
    return schema


def camelize_schema_variants(schema: dict[str, Any]) -> dict[str, Any]:
    for keyword in ("allOf", "anyOf", "oneOf"):
        if keyword in schema:
            schema[keyword] = [camelize_schema(item) for item in schema[keyword]]
    return schema


def camelize_schema(schema: dict[str, Any]) -> dict[str, Any]:
    schema = camelize_schema_properties(schema)
    return camelize_schema_variants(schema)
