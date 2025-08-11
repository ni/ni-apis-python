import pytest
from nitypes.vector import Vector

import ni.protobuf.types.vector_pb2 as vector_pb2
from ni.protobuf.types.attribute_value_pb2 import AttributeValue
from ni.protobuf.types.vector_conversion import vector_from_protobuf, vector_to_protobuf


# ========================================================
# Scalar: Protobuf to Python
# ========================================================
def test___bool_vector_protobuf___convert___valid_bool_vector() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    expected_value = [True, False]
    protobuf_value = vector_pb2.Vector(
        attributes=attributes,
        bool_array=vector_pb2.Vector.BoolArray(values=expected_value),
    )

    python_value = vector_from_protobuf(protobuf_value)

    assert isinstance(python_value, Vector)
    assert isinstance(python_value[0], bool)
    assert len(python_value) == 2
    assert list(python_value) == expected_value
    assert python_value.units == "Volts"


def test___int32_vector_protobuf___convert___valid_int_vector() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    expected_value = [10, 20, 30]
    protobuf_value = vector_pb2.Vector(
        attributes=attributes,
        int32_array=vector_pb2.Vector.Int32Array(values=expected_value),
    )

    python_value = vector_from_protobuf(protobuf_value)

    assert isinstance(python_value, Vector)
    assert isinstance(python_value[0], int)
    assert len(python_value) == 3
    assert list(python_value) == expected_value
    assert python_value.units == "Volts"


def test___double_vector_protobuf___convert___valid_float_vector() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    expected_value = [20.0, 30.0, 40.5]
    protobuf_value = vector_pb2.Vector(
        attributes=attributes,
        double_array=vector_pb2.Vector.DoubleArray(values=expected_value),
    )

    python_value = vector_from_protobuf(protobuf_value)

    assert isinstance(python_value, Vector)
    assert isinstance(python_value[0], float)
    assert len(python_value) == 3
    assert list(python_value) == expected_value
    assert python_value.units == "Volts"


def test___string_vector_protobuf___convert___valid_str_vector() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    expected_value = ["one"]
    protobuf_value = vector_pb2.Vector(
        attributes=attributes,
        string_array=vector_pb2.Vector.StringArray(values=expected_value),
    )

    python_value = vector_from_protobuf(protobuf_value)

    assert isinstance(python_value, Vector)
    assert isinstance(python_value[0], str)
    assert len(python_value) == 1
    assert list(python_value) == expected_value
    assert python_value.units == "Volts"


def test___vector_protobuf_value_unset___convert___throws_value_error() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    protobuf_value = vector_pb2.Vector(attributes=attributes)

    with pytest.raises(ValueError) as exc:
        _ = vector_from_protobuf(protobuf_value)

    assert exc.value.args[0].startswith("Could not determine the data type of 'value'.")


def test___vector_protobuf_units_unset___convert___python_units_blank() -> None:
    expected_value = [True, False]
    protobuf_value = vector_pb2.Vector(
        bool_array=vector_pb2.Vector.BoolArray(values=expected_value)
    )

    python_value = vector_from_protobuf(protobuf_value)

    assert isinstance(python_value, Vector)
    assert isinstance(python_value[0], bool)
    assert len(python_value) == 2
    assert list(python_value) == expected_value
    assert python_value.units == ""


def test___vector_with_non_units_attributes___to_python___attributes_converted() -> None:
    attributes = {
        "NI_ChannelName": AttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": AttributeValue(string_value="Volts"),
    }
    expected_value = ["one", "two", "three"]
    protobuf_value = vector_pb2.Vector(
        attributes=attributes,
        string_array=vector_pb2.Vector.StringArray(values=expected_value),
    )

    python_value = vector_from_protobuf(protobuf_value)
    channel_name = python_value.extended_properties["NI_ChannelName"]

    assert isinstance(python_value, Vector)
    assert isinstance(python_value[0], str)
    assert len(python_value) == 3
    assert list(python_value) == expected_value
    assert python_value.units == "Volts"
    assert isinstance(channel_name, str)
    assert channel_name == "Dev1/ai0"


# ========================================================
# Vector: Python to Protobuf
# ========================================================
def test___bool_vector___convert___valid_bool_vector_protobuf() -> None:
    python_value = Vector([True, False], "Volts")

    protobuf_value = vector_to_protobuf(python_value)

    assert isinstance(protobuf_value, vector_pb2.Vector)
    assert protobuf_value.WhichOneof("value") == "bool_array"
    assert protobuf_value.bool_array.values == [True, False]
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"


def test___int_vector___convert___valid_int32_vector_protobuf() -> None:
    python_value = Vector([10, 20, 30], "Volts")

    protobuf_value = vector_to_protobuf(python_value)

    assert isinstance(protobuf_value, vector_pb2.Vector)
    assert protobuf_value.WhichOneof("value") == "int32_array"
    assert protobuf_value.int32_array.values == [10, 20, 30]
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"


def test___float_vector___convert___valid_double_vector_protobuf() -> None:
    python_value = Vector([20.0, 30.0, 40.5], "Volts")

    protobuf_value = vector_to_protobuf(python_value)

    assert isinstance(protobuf_value, vector_pb2.Vector)
    assert protobuf_value.WhichOneof("value") == "double_array"
    assert protobuf_value.double_array.values == [20.0, 30.0, 40.5]
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"


def test___str_vector___convert___valid_string_vector_protobuf() -> None:
    python_value = Vector(["one", "two", "three"], "Volts")

    protobuf_value = vector_to_protobuf(python_value)

    assert isinstance(protobuf_value, vector_pb2.Vector)
    assert protobuf_value.WhichOneof("value") == "string_array"
    assert protobuf_value.string_array.values == ["one", "two", "three"]
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"


def test___vector_units_unset___convert___protobuf_units_blank() -> None:
    python_value = Vector([10, 20, 30])

    protobuf_value = vector_to_protobuf(python_value)

    assert isinstance(protobuf_value, vector_pb2.Vector)
    assert protobuf_value.WhichOneof("value") == "int32_array"
    assert protobuf_value.int32_array.values == [10, 20, 30]
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == ""


def test___vector_with_non_units_attributes___to_protobuf___attributes_converted() -> None:
    python_value = Vector(["value"], "Volts")
    python_value.extended_properties["NI_ChannelName"] = "Dev1/ai0"

    protobuf_value = vector_to_protobuf(python_value)

    assert isinstance(protobuf_value, vector_pb2.Vector)
    assert protobuf_value.WhichOneof("value") == "string_array"
    assert protobuf_value.string_array.values == ["value"]
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"
    assert protobuf_value.attributes["NI_ChannelName"].string_value == "Dev1/ai0"


def test___empty_vector___to_protobuf___raises_value_error() -> None:
    python_value = Vector([], "Volts", value_type=int)

    with pytest.raises(ValueError) as exc:
        _ = vector_to_protobuf(python_value)

    assert exc.value.args[0].startswith("Cannot convert an empty vector.")


def test___int_vector_out_of_range___convert___raises_value_error() -> None:
    python_value = Vector([10, 20, 0x8FFFFFFF], "Volts")

    with pytest.raises(ValueError) as exc:
        _ = vector_to_protobuf(python_value)

    assert exc.value.args[0].startswith(
        "Integer values in a vector must be within the range of an Int32."
    )
