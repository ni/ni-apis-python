"""Tests for the ni.protobuf.types package."""
from src.ni.protobuf.types.array_pb2 import Double2DArray, String2DArray
from src.ni.protobuf.types.precision_timestamp_pb2 import PrecisionTimestamp
from src.ni.protobuf.types.waveform_pb2 import DoubleAnalogWaveform, DoubleComplexWaveform, DoubleSpectrum, I16AnalogWaveform, I16ComplexWaveform, WaveformAttributeValue
from src.ni.protobuf.types.xydata_pb2 import DoubleXYData

EXPECTED_T0 = PrecisionTimestamp(seconds=5, fractional_seconds=0)
EXPECTED_DT = 0.01
EXPECTED_ATTRIBUTES = {
    "attr1": WaveformAttributeValue(integer_value=1),
    "attr2": WaveformAttributeValue(string_value="two"),
}

def test___valid_inputs___createdouble2darray___creation_successful() -> None:
    test_array = Double2DArray(rows=2, columns=2, data=[1.0, 2.0, 3.0, 4.0])

    assert test_array.rows == test_array.columns == 2
    assert list(test_array.data) == [1.0, 2.0, 3.0, 4.0]


def test___valid_inputs___createstring2darray___creation_successful() -> None:
    test_array = String2DArray(rows=2, columns=2, data=["A", "B", "C", "D"])

    assert test_array.rows == test_array.columns == 2
    assert list(test_array.data) == ["A", "B", "C", "D"]


def test___valid_inputs___create_doubleanalogwaveform___creation_successful() -> None:
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


def test___valid_inputs___create_i16analogwaveform___creation_successful() -> None:
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


def test___valid_inputs___create_doublecomplexwaveform___creation_successful() -> None:
    test_wfm = DoubleComplexWaveform(
        t0=EXPECTED_T0,
        dt=EXPECTED_DT,
        y_data=[1.0, 2.0, 3.0],
        attributes=EXPECTED_ATTRIBUTES,
    )

    assert test_wfm.t0 == EXPECTED_T0
    assert test_wfm.dt == EXPECTED_DT
    assert list(test_wfm.y_data) == [1.0, 2.0, 3.0]
    assert test_wfm.attributes == EXPECTED_ATTRIBUTES


def test___valid_inputs___create_i16complexwaveform___creation_successful() -> None:
    test_wfm = I16ComplexWaveform(
        t0=EXPECTED_T0,
        dt=EXPECTED_DT,
        y_data=[1, 2, 3],
        attributes=EXPECTED_ATTRIBUTES,
    )

    assert test_wfm.t0 == EXPECTED_T0
    assert test_wfm.dt == EXPECTED_DT
    assert list(test_wfm.y_data) == [1, 2, 3]
    assert test_wfm.attributes == EXPECTED_ATTRIBUTES


def test___valid_inputs___create_doublespectrum___creation_successful() -> None:
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


def test___valid_inputs___create_doublexydata___creation_successful() -> None:
    test_wfm = DoubleXYData(
        x_data=[1.0, 2.0, 3.0],
        y_data=[4.0, 5.0, 6.0],
    )

    assert list(test_wfm.x_data) == [1.0, 2.0, 3.0]
    assert list(test_wfm.y_data) == [4.0, 5.0, 6.0]
