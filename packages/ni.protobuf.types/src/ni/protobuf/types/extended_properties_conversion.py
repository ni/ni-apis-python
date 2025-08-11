"""Methods to convert between ExtendedPropertyDictionaries and AttributeValue maps."""

from __future__ import annotations

from collections.abc import Mapping

from nitypes.waveform import ExtendedPropertyDictionary
from nitypes.waveform.typing import ExtendedPropertyValue

from ni.protobuf.types.attribute_value_pb2 import AttributeValue


def extended_properties_to_protobuf(
    extended_properties: ExtendedPropertyDictionary,
) -> dict[str, AttributeValue]:
    """Convert an ExtendedPropertyDictionary to an AttributeValue map."""
    return {key: _value_to_attribute(value) for key, value in extended_properties.items()}


def _value_to_attribute(value: ExtendedPropertyValue) -> AttributeValue:
    attr_value = AttributeValue()
    if isinstance(value, bool):
        attr_value.bool_value = value
    elif isinstance(value, int):
        attr_value.integer_value = value
    elif isinstance(value, float):
        attr_value.double_value = value
    elif isinstance(value, str):
        attr_value.string_value = value
    else:
        raise TypeError(f"Unexpected type for extended property value {type(value)}")

    return attr_value


def extended_properties_from_protobuf(
    attributes: Mapping[str, AttributeValue],
    extended_properties: ExtendedPropertyDictionary,
) -> None:
    """Convert an AttributeValue map and insert values into an ExtendedPropertyDictionary."""
    for key, value in attributes.items():
        attr_type = value.WhichOneof("attribute")
        if attr_type is None:
            raise ValueError("Could not determine the data type of 'attribute'.")
        extended_properties[key] = getattr(value, attr_type)
