"""Tests for the ni.protobuf.types package."""

from ni.protobuf.types.array_pb2 import Double2DArray, String2DArray
from ni.protobuf.types.attribute_value_pb2 import AttributeValue
from ni.protobuf.types.precision_timestamp_pb2 import PrecisionTimestamp
from ni.protobuf.types.scalar_pb2 import Scalar
from ni.protobuf.types.waveform_pb2 import (
    DoubleAnalogWaveform,
    DoubleComplexWaveform,
    DoubleSpectrum,
    I16AnalogWaveform,
    I16ComplexWaveform,
    WaveformAttributeValue,
)
from ni.protobuf.types.xydata_pb2 import DoubleXYData

EXPECTED_T0 = PrecisionTimestamp(seconds=5, fractional_seconds=0)
EXPECTED_DT = 0.01
EXPECTED_ATTRIBUTES = {
    "attr1": WaveformAttributeValue(integer_value=1),
    "attr2": WaveformAttributeValue(string_value="two"),
}
EXPECTED_SCALAR_ATTRIBUTES = {
    "attr1": AttributeValue(integer_value=1),
    "attr2": AttributeValue(string_value="two"),
}


def test___valid_inputs___createdouble2darray___message_created() -> None:
    test_array = Double2DArray(rows=3, columns=2, data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

    assert test_array.rows == 3
    assert test_array.columns == 2
    assert list(test_array.data) == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]


def test___valid_inputs___createstring2darray___message_created() -> None:
    test_array = String2DArray(rows=2, columns=3, data=["A", "B", "C", "D", "E", "F"])

    assert test_array.rows == 2
    assert test_array.columns == 3
    assert list(test_array.data) == ["A", "B", "C", "D", "E", "F"]


def test___valid_inputs___create_doubleanalogwaveform___message_created() -> None:
    test_wfm = DoubleAnalogWaveform(
        t0=EXPECTED_T0,
        dt=EXPECTED_DT,
        y_data=[1.0, 2.0, 3.0],
        attributes=EXPECTED_ATTRIBUTES,
    )

    assert test_wfm.t0 == EXPECTED_T0
    assert test_wfm.dt == EXPECTED_DT
    assert list(test_wfm.y_data) == [1.0, 2.0, 3.0]
    assert test_wfm.attributes == EXPECTED_ATTRIBUTES


def test___valid_inputs___create_i16analogwaveform___message_created() -> None:
    test_wfm = I16AnalogWaveform(
        t0=EXPECTED_T0,
        dt=EXPECTED_DT,
        y_data=[1, 2, 3],
        attributes=EXPECTED_ATTRIBUTES,
    )

    assert test_wfm.t0 == EXPECTED_T0
    assert test_wfm.dt == EXPECTED_DT
    assert list(test_wfm.y_data) == [1, 2, 3]
    assert test_wfm.attributes == EXPECTED_ATTRIBUTES


def test___valid_inputs___create_doublecomplexwaveform___message_created() -> None:
    test_wfm = DoubleComplexWaveform(
        t0=EXPECTED_T0,
        dt=EXPECTED_DT,
        y_data=[1.0, 2.0, 3.0, 4.0],
        attributes=EXPECTED_ATTRIBUTES,
    )

    assert test_wfm.t0 == EXPECTED_T0
    assert test_wfm.dt == EXPECTED_DT
    assert list(test_wfm.y_data) == [1.0, 2.0, 3.0, 4.0]
    assert test_wfm.attributes == EXPECTED_ATTRIBUTES


def test___valid_inputs___create_i16complexwaveform___message_created() -> None:
    test_wfm = I16ComplexWaveform(
        t0=EXPECTED_T0,
        dt=EXPECTED_DT,
        y_data=[1, 2, 3, 4],
        attributes=EXPECTED_ATTRIBUTES,
    )

    assert test_wfm.t0 == EXPECTED_T0
    assert test_wfm.dt == EXPECTED_DT
    assert list(test_wfm.y_data) == [1, 2, 3, 4]
    assert test_wfm.attributes == EXPECTED_ATTRIBUTES


def test___valid_inputs___create_doublespectrum___message_created() -> None:
    test_wfm = DoubleSpectrum(
        start_frequency=10.0,
        frequency_increment=1.0,
        data=[1.0, 2.0, 3.0],
        attributes=EXPECTED_ATTRIBUTES,
    )

    assert test_wfm.start_frequency == 10.0
    assert test_wfm.frequency_increment == 1.0
    assert list(test_wfm.data) == [1.0, 2.0, 3.0]
    assert test_wfm.attributes == EXPECTED_ATTRIBUTES


def test___valid_inputs___create_doublexydata___message_created() -> None:
    test_wfm = DoubleXYData(
        x_data=[1.0, 2.0, 3.0],
        y_data=[4.0, 5.0, 6.0],
    )

    assert list(test_wfm.x_data) == [1.0, 2.0, 3.0]
    assert list(test_wfm.y_data) == [4.0, 5.0, 6.0]


def test___valid_inputs___create_double_scalar___message_created() -> None:
    test_scalar = Scalar(attributes=EXPECTED_SCALAR_ATTRIBUTES, double_value=1.0)

    assert test_scalar.double_value == 1.0
    assert test_scalar.attributes == EXPECTED_SCALAR_ATTRIBUTES


def test___valid_inputs___create_int_scalar___message_created() -> None:
    test_scalar = Scalar(attributes=EXPECTED_SCALAR_ATTRIBUTES, int32_value=1)

    assert test_scalar.int32_value == 1
    assert test_scalar.attributes == EXPECTED_SCALAR_ATTRIBUTES


def test___valid_inputs___create_bool_scalar___message_created() -> None:
    test_scalar = Scalar(attributes=EXPECTED_SCALAR_ATTRIBUTES, bool_value=True)

    assert test_scalar.bool_value is True
    assert test_scalar.attributes == EXPECTED_SCALAR_ATTRIBUTES


def test___valid_inputs___create_string_scalar___message_created() -> None:
    test_scalar = Scalar(attributes=EXPECTED_SCALAR_ATTRIBUTES, string_value="one")

    assert test_scalar.string_value == "one"
    assert test_scalar.attributes == EXPECTED_SCALAR_ATTRIBUTES
