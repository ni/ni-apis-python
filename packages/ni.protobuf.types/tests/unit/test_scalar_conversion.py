import pytest
from nitypes.scalar import Scalar

import ni.protobuf.types.scalar_pb2 as scalar_pb2
from ni.protobuf.types.attribute_value_pb2 import AttributeValue
from ni.protobuf.types.scalar_conversion import scalar_from_protobuf, scalar_to_protobuf


# ========================================================
# Scalar: Protobuf to Python
# ========================================================
def test___bool_scalar_protobuf___convert___valid_bool_scalar() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    protobuf_value = scalar_pb2.Scalar(attributes=attributes)
    protobuf_value.bool_value = True

    python_value = scalar_from_protobuf(protobuf_value)

    assert isinstance(python_value.value, bool)
    assert python_value.value is True
    assert python_value.units == "Volts"


def test___int32_scalar_protobuf___convert___valid_int_scalar() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    protobuf_value = scalar_pb2.Scalar(attributes=attributes)
    protobuf_value.int32_value = 10

    python_value = scalar_from_protobuf(protobuf_value)

    assert isinstance(python_value.value, int)
    assert python_value.value == 10
    assert python_value.units == "Volts"


def test___double_scalar_protobuf___convert___valid_float_scalar() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    protobuf_value = scalar_pb2.Scalar(attributes=attributes)
    protobuf_value.double_value = 20.0

    python_value = scalar_from_protobuf(protobuf_value)

    assert isinstance(python_value.value, float)
    assert python_value.value == 20.0
    assert python_value.units == "Volts"


def test___string_scalar_protobuf___convert___valid_str_scalar() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    protobuf_value = scalar_pb2.Scalar(attributes=attributes)
    protobuf_value.string_value = "value"

    python_value = scalar_from_protobuf(protobuf_value)

    assert isinstance(python_value.value, str)
    assert python_value.value == "value"
    assert python_value.units == "Volts"


def test___scalar_protobuf_value_unset___convert___throws_value_error() -> None:
    attributes = {"NI_UnitDescription": AttributeValue(string_value="Volts")}
    protobuf_value = scalar_pb2.Scalar(attributes=attributes)

    with pytest.raises(ValueError) as exc:
        _ = scalar_from_protobuf(protobuf_value)

    assert exc.value.args[0].startswith("Could not determine the data type of 'value'.")


def test___scalar_protobuf_units_unset___convert___python_units_blank() -> None:
    protobuf_value = scalar_pb2.Scalar()
    protobuf_value.bool_value = True

    python_value = scalar_from_protobuf(protobuf_value)

    assert isinstance(python_value.value, bool)
    assert python_value.value is True
    assert python_value.units == ""


def test___non_units_attributes___to_python___attributes_converted() -> None:
    attributes = {
        "NI_ChannelName": AttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": AttributeValue(string_value="Volts"),
    }
    protobuf_value = scalar_pb2.Scalar(attributes=attributes)
    protobuf_value.string_value = "value"

    python_value = scalar_from_protobuf(protobuf_value)
    channel_name = python_value.extended_properties["NI_ChannelName"]

    assert isinstance(python_value.value, str)
    assert python_value.value == "value"
    assert python_value.units == "Volts"
    assert isinstance(channel_name, str)
    assert channel_name == "Dev1/ai0"


# ========================================================
# Scalar: Python to Protobuf
# ========================================================
def test___bool_scalar___convert___valid_bool_scalar_protobuf() -> None:
    python_value = Scalar(True, "Volts")

    protobuf_value = scalar_to_protobuf(python_value)

    assert protobuf_value.WhichOneof("value") == "bool_value"
    assert protobuf_value.bool_value is True
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"


def test___int_scalar___convert___valid_int32_scalar_protobuf() -> None:
    python_value = Scalar(10, "Volts")

    protobuf_value = scalar_to_protobuf(python_value)

    assert protobuf_value.WhichOneof("value") == "int32_value"
    assert protobuf_value.int32_value == 10
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"


def test___float_scalar___convert___valid_double_scalar_protobuf() -> None:
    python_value = Scalar(20.0, "Volts")

    protobuf_value = scalar_to_protobuf(python_value)

    assert protobuf_value.WhichOneof("value") == "double_value"
    assert protobuf_value.double_value == 20.0
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"


def test___str_scalar___convert___valid_string_scalar_protobuf() -> None:
    python_value = Scalar("value", "Volts")

    protobuf_value = scalar_to_protobuf(python_value)

    assert protobuf_value.WhichOneof("value") == "string_value"
    assert protobuf_value.string_value == "value"
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"


def test___scalar_units_unset___convert___protobuf_units_blank() -> None:
    python_value = Scalar(10)

    protobuf_value = scalar_to_protobuf(python_value)

    assert protobuf_value.WhichOneof("value") == "int32_value"
    assert protobuf_value.int32_value == 10
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == ""


def test___non_units_attributes___to_protobuf___attributes_converted() -> None:
    python_value = Scalar("value", "Volts")
    python_value.extended_properties["NI_ChannelName"] = "Dev1/ai0"

    protobuf_value = scalar_to_protobuf(python_value)

    assert protobuf_value.WhichOneof("value") == "string_value"
    assert protobuf_value.string_value == "value"
    assert protobuf_value.attributes["NI_UnitDescription"].string_value == "Volts"
    assert protobuf_value.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
