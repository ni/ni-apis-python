import numpy as np
from nitypes.xy_data import XYData

import ni.protobuf.types.xydata_pb2 as xydata_pb2
from ni.protobuf.types.attribute_value_pb2 import AttributeValue
from ni.protobuf.types.xydata_conversion import (
    float64_xydata_from_protobuf,
    float64_xydata_to_protobuf,
)


# ========================================================
# XYData: Protobuf to Python
# ========================================================
def test___doublexydata_protobuf___convert___valid_xydata_default_units() -> None:
    expected_x_data = [1.0, 2.0, 3.0]
    expected_y_data = [4.0, 5.0, 6.0]
    protobuf_value = xydata_pb2.DoubleXYData(x_data=expected_x_data, y_data=expected_y_data)

    python_value = float64_xydata_from_protobuf(protobuf_value)
    assert isinstance(python_value, XYData)
    assert python_value.dtype == np.float64
    assert list(python_value.x_data) == expected_x_data
    assert list(python_value.y_data) == expected_y_data
    assert python_value.x_units == ""
    assert python_value.y_units == ""


def test___doublexydata_protobuf_with_units___convert___valid_xydata() -> None:
    attributes = {
        "NI_UnitDescription_X": AttributeValue(string_value="Volts"),
        "NI_UnitDescription_Y": AttributeValue(string_value="Seconds"),
    }
    expected_x_data = [1.0, 2.0, 3.0]
    expected_y_data = [4.0, 5.0, 6.0]
    protobuf_value = xydata_pb2.DoubleXYData(
        x_data=expected_x_data,
        y_data=expected_y_data,
        attributes=attributes,
    )

    python_value = float64_xydata_from_protobuf(protobuf_value)

    assert isinstance(python_value, XYData)
    assert python_value.dtype == np.float64
    assert list(python_value.x_data) == expected_x_data
    assert list(python_value.y_data) == expected_y_data
    assert python_value.x_units == "Volts"
    assert python_value.y_units == "Seconds"


def test___doublexydata_protobuf_with_other_attrs___convert___attrs_converted() -> None:
    attributes = {
        "NI_UnitDescription_X": AttributeValue(string_value="Volts"),
        "NI_UnitDescription_Y": AttributeValue(string_value="Seconds"),
        "Non_Units_Attribute": AttributeValue(double_value=1.1),
    }
    protobuf_value = xydata_pb2.DoubleXYData(
        x_data=[1.0],
        y_data=[2.0],
        attributes=attributes,
    )

    python_value = float64_xydata_from_protobuf(protobuf_value)

    assert isinstance(python_value, XYData)
    assert python_value.x_units == "Volts"
    assert python_value.y_units == "Seconds"
    assert python_value.extended_properties.get("Non_Units_Attribute") == 1.1


# ========================================================
# XYData: Python to Protobuf
# ========================================================
def test___float64_xydata___convert___valid_doublexydata_protobuf() -> None:
    expected_x_data = [1.0, 2.0, 3.0]
    expected_y_data = [4.0, 5.0, 6.0]
    python_value = XYData.from_arrays_1d(
        x_array=expected_x_data,
        y_array=expected_y_data,
        dtype=np.float64,
    )

    protobuf_value = float64_xydata_to_protobuf(python_value)

    assert isinstance(protobuf_value, xydata_pb2.DoubleXYData)
    assert list(protobuf_value.x_data) == expected_x_data
    assert list(protobuf_value.y_data) == expected_y_data


def test___int16_xydata___convert___valid_doublexydata_protobuf() -> None:
    python_value = XYData.from_arrays_1d(
        x_array=[1, 2, 3],
        y_array=[4, 5, 6],
        dtype=np.int16,
    )

    protobuf_value = float64_xydata_to_protobuf(python_value)

    assert isinstance(protobuf_value, xydata_pb2.DoubleXYData)
    # Data values converted to float. Is this OK? Or should we raise an error here?
    assert list(protobuf_value.x_data) == [1.0, 2.0, 3.0]
    assert list(protobuf_value.y_data) == [4.0, 5.0, 6.0]


def test___xydata_with_extended_properties___convert___valid_doublexydata_protobuf() -> None:
    expected_x_data = [1.0]
    expected_y_data = [2.0]
    python_value = XYData.from_arrays_1d(
        x_array=expected_x_data,
        y_array=expected_y_data,
        dtype=np.float64,
        extended_properties={
            "true": True,
            "1": 1,
            "1.0": 1.0,
            "str": "str",
        },
    )

    protobuf_value = float64_xydata_to_protobuf(python_value)

    assert isinstance(protobuf_value, xydata_pb2.DoubleXYData)
    assert list(protobuf_value.x_data) == expected_x_data
    assert list(protobuf_value.y_data) == expected_y_data
    assert protobuf_value.attributes["true"].bool_value is True
    assert protobuf_value.attributes["1"].integer_value == 1
    assert protobuf_value.attributes["1.0"].double_value == 1.0
    assert protobuf_value.attributes["str"].string_value == "str"
