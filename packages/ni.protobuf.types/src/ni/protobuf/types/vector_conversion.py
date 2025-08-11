"""Methods to convert to and from scalar protobuf messages."""

from __future__ import annotations

from typing import Any, MutableSequence, cast

from nitypes.vector import Vector

import ni.protobuf.types.vector_pb2 as vector_pb2
from ni.protobuf.types.attribute_value_conversion import (
    attributes_to_extended_properties,
    extended_properties_to_attributes,
)
from ni.protobuf.types.attribute_value_pb2 import AttributeValue
from ni.protobuf.types.scalar_conversion import AnyScalarType, check_scalar_value

_VECTOR_TYPE_TO_PB_ATTR_MAP = {
    bool: "bool_array",
    int: "int32_array",
    float: "double_array",
    str: "string_array",
}


def vector_to_protobuf(value: Vector[Any], /) -> vector_pb2.Vector:
    """Convert a Vector python object to a protobuf vector_pb2.Vector."""
    if not len(value):
        raise ValueError("Cannot convert an empty vector.")

    _check_vector_values(value)
    return _create_vector_message(
        attributes=extended_properties_to_attributes(value.extended_properties),
        array_value=value[0:],
    )


def vector_from_protobuf(message: vector_pb2.Vector, /) -> Vector[AnyScalarType]:
    """Convert the protobuf vector_pb2.Vector to a Python Vector."""
    pb_type = message.WhichOneof("value")
    if pb_type is None:
        raise ValueError("Could not determine the data type of 'value'.")

    if pb_type not in _VECTOR_TYPE_TO_PB_ATTR_MAP.values():
        raise ValueError(f"Unexpected value for protobuf_value.WhichOneOf: {pb_type}")

    value: (
        vector_pb2.Vector.BoolArray
        | vector_pb2.Vector.Int32Array
        | vector_pb2.Vector.DoubleArray
        | vector_pb2.Vector.StringArray
    )
    value = getattr(message, pb_type)

    # Create with blank units. Units from the protobuf message will be populated
    # when attributes are converted to an ExtendedPropertyDictionary.
    vector = Vector(value.values, "")

    # Transfer attributes to extended_properties
    attributes_to_extended_properties(message.attributes, vector.extended_properties)

    return vector


def _create_vector_message(
    attributes: dict[str, AttributeValue],
    array_value: MutableSequence[AnyScalarType],
) -> vector_pb2.Vector:
    """Create a vector_pb2 object with the given value and value_type.

    This method was created Because creating a Vector requires passing
    in a type specific array object.

    This method assumes that all values of array_value are of the same type.
    """
    if isinstance(array_value[0], bool):
        bool_seq = cast(MutableSequence[bool], array_value)
        bool_array = vector_pb2.Vector.BoolArray(values=bool_seq)
        return vector_pb2.Vector(attributes=attributes, bool_array=bool_array)
    elif isinstance(array_value[0], int):
        int_seq = cast(MutableSequence[int], array_value)
        int_array = vector_pb2.Vector.Int32Array(values=int_seq)
        return vector_pb2.Vector(attributes=attributes, int32_array=int_array)
    elif isinstance(array_value[0], float):
        double_seq = cast(MutableSequence[float], array_value)
        double_array = vector_pb2.Vector.DoubleArray(values=double_seq)
        return vector_pb2.Vector(attributes=attributes, double_array=double_array)
    elif isinstance(array_value[0], str):
        string_seq = cast(MutableSequence[str], array_value)
        string_array = vector_pb2.Vector.StringArray(values=string_seq)
        return vector_pb2.Vector(attributes=attributes, string_array=string_array)
    else:
        raise TypeError(f"Invalid array value type: {type(array_value[0])}")


def _check_vector_values(vector: Vector[AnyScalarType]) -> None:
    for value in vector:
        check_scalar_value(value)
