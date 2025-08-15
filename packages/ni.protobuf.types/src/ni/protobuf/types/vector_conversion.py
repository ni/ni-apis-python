"""Methods to convert to and from scalar protobuf messages."""

from __future__ import annotations

from typing import Any, cast

from nitypes.vector import Vector

import ni.protobuf.types.array_pb2 as array_pb2
import ni.protobuf.types.vector_pb2 as vector_pb2
from ni.protobuf.types.attribute_value_pb2 import AttributeValue
from ni.protobuf.types.extended_property_conversion import (
    extended_properties_from_protobuf,
    extended_properties_to_protobuf,
)
from ni.protobuf.types.scalar_conversion import AnyScalarType

_VECTOR_TYPE_TO_PB_ATTR_MAP = {
    bool: "bool_array",
    int: "sint32_array",
    float: "double_array",
    str: "string_array",
}


def vector_to_protobuf(value: Vector[Any], /) -> vector_pb2.Vector:
    """Convert a Vector python object to a protobuf vector_pb2.Vector."""
    if not len(value):
        raise ValueError("Cannot convert an empty vector.")

    _check_vector_values(value)
    attributes = extended_properties_to_protobuf(value.extended_properties)
    return _create_vector_message(value, attributes)


def vector_from_protobuf(message: vector_pb2.Vector, /) -> Vector[AnyScalarType]:
    """Convert the protobuf vector_pb2.Vector to a Python Vector."""
    pb_type = message.WhichOneof("value")
    if pb_type is None:
        raise ValueError("Could not determine the data type of 'value'.")

    if pb_type not in _VECTOR_TYPE_TO_PB_ATTR_MAP.values():
        raise ValueError(f"Unexpected value for protobuf_value.WhichOneOf: {pb_type}")

    value: (
        array_pb2.BoolArray | array_pb2.SInt32Array | array_pb2.DoubleArray | array_pb2.StringArray
    )
    value = getattr(message, pb_type)

    # Create with blank units. Units from the protobuf message will be populated
    # when attributes are converted to an ExtendedPropertyDictionary.
    vector = Vector(value.values, "")

    # Transfer attributes to extended_properties
    extended_properties_from_protobuf(message.attributes, vector.extended_properties)

    return vector


def _create_vector_message(
    vector_obj: Vector[Any],
    attributes: dict[str, AttributeValue],
) -> vector_pb2.Vector:
    if isinstance(vector_obj[0], bool):
        bool_vector = cast(Vector[bool], vector_obj)
        bool_array = array_pb2.BoolArray(values=bool_vector)
        return vector_pb2.Vector(attributes=attributes, bool_array=bool_array)
    elif isinstance(vector_obj[0], int):
        int_vector = cast(Vector[int], vector_obj)
        int_array = array_pb2.SInt32Array(values=int_vector)
        return vector_pb2.Vector(attributes=attributes, sint32_array=int_array)
    elif isinstance(vector_obj[0], float):
        double_vector = cast(Vector[float], vector_obj)
        double_array = array_pb2.DoubleArray(values=double_vector)
        return vector_pb2.Vector(attributes=attributes, double_array=double_array)
    elif isinstance(vector_obj[0], str):
        string_vector = cast(Vector[str], vector_obj)
        string_array = array_pb2.StringArray(values=string_vector)
        return vector_pb2.Vector(attributes=attributes, string_array=string_array)
    else:
        raise TypeError(f"Invalid array value type: {type(vector_obj[0])}")


def _check_vector_values(vector: Vector[AnyScalarType]) -> None:
    for value in vector:
        if isinstance(value, int):
            if value <= -0x80000000 or value >= 0x7FFFFFFF:
                raise ValueError("Integer values in a vector must be within the range of an Int32.")
