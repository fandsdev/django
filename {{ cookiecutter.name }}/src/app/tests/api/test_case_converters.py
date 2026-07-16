import pytest
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

from app.api.case_converters import camel_to_snake, camelize_keys, snake_to_camel, snakeize_keys, snakeize_query_dict


@pytest.mark.parametrize(
    ("snake", "camel"),
    [
        ("first_name", "firstName"),
        ("home_address_zip", "homeAddressZip"),
        ("field2_name", "field2Name"),
        ("plain", "plain"),
        ("child_uuid", "childUuid"),
    ],
)
def test_key_conversion_round_trip(snake, camel):
    assert snake_to_camel(snake) == camel
    assert camel_to_snake(camel) == snake


def test_camelize_keys_nested():
    data = {"user_profile": {"first_name": "John", "home_address": {"zip_code": "12345"}}, "tags": [{"tag_name": "a"}]}

    assert camelize_keys(data) == {"userProfile": {"firstName": "John", "homeAddress": {"zipCode": "12345"}}, "tags": [{"tagName": "a"}]}


def test_snakeize_keys_nested():
    data = {"userProfile": {"firstName": "John"}, "items": [{"zipCode": "1"}]}

    assert snakeize_keys(data) == {"user_profile": {"first_name": "John"}, "items": [{"zip_code": "1"}]}


def test_camelize_keys_leaves_non_string_keys():
    assert camelize_keys({1: "a", "b_c": "d"}) == {1: "a", "bC": "d"}


def test_snakeize_query_dict_returns_query_dict():
    source = QueryDict("firstName=John&firstName=Jane&lastName=Doe")

    result = snakeize_query_dict(source)

    assert isinstance(result, QueryDict)
    assert result.getlist("first_name") == ["John", "Jane"]
    assert result["last_name"] == "Doe"


def test_snakeize_query_dict_returns_multi_value_dict():
    source = MultiValueDict({"fieldName": ["value1", "value2"]})

    result = snakeize_query_dict(source)

    assert isinstance(result, MultiValueDict)
    assert not isinstance(result, QueryDict)
    assert result.getlist("field_name") == ["value1", "value2"]


def test_snake_to_camel_digit_word_is_not_reversible():
    assert snake_to_camel("address_2") == "address2"
    assert camel_to_snake("address2") == "address2"
