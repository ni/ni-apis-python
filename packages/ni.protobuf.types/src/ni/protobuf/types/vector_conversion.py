"""Methods to convert to and from scalar protobuf messages."""

from __future__ import annotations

from nitypes.vector import Vector
from typing_extensions import Mapping, Iterable

import ni.protobuf.types.vector_pb2 as vector_pb2
from ni.protobuf.types.attribute_value_pb2 import AttributeValue
from ni.protobuf.types.attribute_value_conversion import (
    extended_properties_to_attributes,
    attributes_to_extended_properties,
)
from ni.protobuf.types.scalar_conversion import AnyScalarType, check_scalar_value

_VECTOR_TYPE_TO_PB_ATTR_MAP = {
    bool: "bool_array",
    int: "int32_array",
    float: "double_array",
    str: "string_array",
}


def vector_to_protobuf(value: Vector[AnyScalarType], /) -> vector_pb2.Vector:
    """Convert a Vector python object to a protobuf vector_pb2.Vector."""
    if not len(value):
        raise ValueError("Cannot convert a vector with no values.")

    _check_vector_values(value)
    return _create_vector(
        attributes=extended_properties_to_attributes(value.extended_properties),
        array_value=value[0:],
        array_value_type=type(value[0]),
    )


def vector_from_protobuf(message: vector_pb2.Vector, /) -> Vector[AnyScalarType]:
    """Convert the protobuf vector_pb2.Vector to a Python Vector."""
    pb_type = message.WhichOneof("value")
    if pb_type is None:
        raise ValueError("Could not determine the data type of 'value'.")

    if pb_type not in _VECTOR_TYPE_TO_PB_ATTR_MAP.values():
        raise ValueError(f"Unexpected value for protobuf_value.WhichOneOf: {pb_type}")
    value = getattr(message, pb_type)

    # Create with blank units. Units from the protobuf message will be populated
    # when attributes are converted to an ExtendedPropertyDictionary.
    scalar = Vector(value, "")

    # Transfer attributes to extended_properties
    attributes_to_extended_properties(message.attributes, scalar.extended_properties)

    return scalar


def _create_vector(
    attributes: dict[str, AttributeValue],
    array_value: Iterable[AnyScalarType],
    array_value_type: type[AnyScalarType],
):
    if array_value_type == bool:
        return vector_pb2.Vector(attributes=attributes, bool_array=array_value)
    elif array_value_type == int:
        return vector_pb2.Vector(attributes=attributes, int32_array=array_value)
    elif array_value_type == float:
        return vector_pb2.Vector(attributes=attributes, double_array=array_value)
    elif array_value_type == str:
        return vector_pb2.Vector(attributes=attributes, string_array=array_value)
    else:
        raise TypeError(f"Invalid array value type: {array_value_type}")


def _check_vector_values(vector: Vector[AnyScalarType]) -> None:
    for value in vector:
        check_scalar_value(value)
