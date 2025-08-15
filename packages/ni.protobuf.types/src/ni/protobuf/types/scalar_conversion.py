"""Methods to convert to and from scalar protobuf messages."""

from __future__ import annotations

from typing import Union

from nitypes.scalar import Scalar
from typing_extensions import TypeAlias

import ni.protobuf.types.scalar_pb2 as scalar_pb2
from ni.protobuf.types.extended_property_conversion import (
    extended_properties_from_protobuf,
    extended_properties_to_protobuf,
)

AnyScalarType: TypeAlias = Union[bool, int, float, str]
_SCALAR_TYPE_TO_PB_ATTR_MAP = {
    bool: "bool_value",
    int: "sint32_value",
    float: "double_value",
    str: "string_value",
}


def scalar_to_protobuf(value: Scalar[AnyScalarType], /) -> scalar_pb2.Scalar:
    """Convert a Scalar python object to a protobuf scalar_pb2.Scalar."""
    attributes = extended_properties_to_protobuf(value.extended_properties)
    message = scalar_pb2.Scalar(attributes=attributes)

    # Convert the scalar value
    _check_scalar_value(value.value)
    value_attr = _SCALAR_TYPE_TO_PB_ATTR_MAP.get(type(value.value), None)
    if not value_attr:
        raise TypeError(f"Unexpected type for value.value: {type(value.value)}")

    setattr(message, value_attr, value.value)

    return message


def scalar_from_protobuf(message: scalar_pb2.Scalar, /) -> Scalar[AnyScalarType]:
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
    extended_properties_from_protobuf(message.attributes, scalar.extended_properties)

    return scalar


def _check_scalar_value(value: AnyScalarType) -> None:
    """Perform value checking on a scalar value."""
    if isinstance(value, int):
        if value <= -0x80000000 or value >= 0x7FFFFFFF:
            raise ValueError("The integer value in a scalar must be within the range of an Int32.")
