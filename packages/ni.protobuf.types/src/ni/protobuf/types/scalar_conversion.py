"""Methods to convert to and from scalar protobuf messages."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Union

from nitypes.scalar import Scalar
from nitypes.waveform import ExtendedPropertyDictionary
from nitypes.waveform.typing import ExtendedPropertyValue
from typing_extensions import TypeAlias

import ni.protobuf.types.scalar_pb2 as scalar_pb2
from ni.protobuf.types.attribute_value_pb2 import AttributeValue

_AnyScalarType: TypeAlias = Union[bool, int, float, str]
_SCALAR_TYPE_TO_PB_ATTR_MAP = {
    bool: "bool_value",
    int: "int32_value",
    float: "double_value",
    str: "string_value",
}


def scalar_to_protobuf(value: Scalar[_AnyScalarType], /) -> scalar_pb2.Scalar:
    """Convert a Scalar python object to a protobuf scalar_pb2.Scalar."""
    attributes = _extended_properties_to_attributes(value.extended_properties)
    message = scalar_pb2.Scalar(attributes=attributes)

    # Convert the scalar value
    value_attr = _SCALAR_TYPE_TO_PB_ATTR_MAP.get(type(value.value), None)
    if not value_attr:
        raise TypeError(f"Unexpected type for python_value.value: {type(value.value)}")
    setattr(message, value_attr, value.value)

    return message


def scalar_from_protobuf(message: scalar_pb2.Scalar, /) -> Scalar[_AnyScalarType]:
    """Convert the protobuf scalar_pb2.Scalar to a Python Scalar."""
    # Convert the scalar value.
    pb_type = message.WhichOneof("value")
    if pb_type is None:
        raise ValueError("Could not determine the data type of 'value'.")

    if pb_type not in _SCALAR_TYPE_TO_PB_ATTR_MAP.values():
        raise ValueError(f"Unexpected value for protobuf_value.WhichOneOf: {pb_type}")
    value = getattr(message, pb_type)

    # Create with blank units. Units from the protobuf message will be populated
    # when attributes are converted to an ExtendedPropertyDictionary.
    scalar = Scalar(value, "")

    # Transfer attributes to extended_properties
    for key, value in message.attributes.items():
        attr_type = value.WhichOneof("attribute")
        if attr_type is None:
            raise ValueError("Could not determine the data type of 'attribute'.")
        scalar.extended_properties[key] = getattr(value, attr_type)

    return scalar


def _extended_properties_to_attributes(
    extended_properties: ExtendedPropertyDictionary,
) -> Mapping[str, AttributeValue]:
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
