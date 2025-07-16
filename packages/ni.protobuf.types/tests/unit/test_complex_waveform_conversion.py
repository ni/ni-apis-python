import datetime as dt

import numpy as np
from nitypes.bintime import DateTime
from nitypes.complex import convert_complex, ComplexInt32Base, ComplexInt32DType
from nitypes.waveform import ComplexWaveform, NoneScaleMode, SampleIntervalMode, Timing

from ni.protobuf.types.precision_timestamp_conversion import bintime_datetime_to_protobuf
from ni.protobuf.types.complex_waveform_conversion import (
    float64_complex_waveform_from_protobuf,
    float64_complex_waveform_to_protobuf,
    int16_complex_waveform_from_protobuf,
    int16_complex_waveform_to_protobuf
)
from ni.protobuf.types.waveform_pb2 import (
    DoubleComplexWaveform,
    WaveformAttributeValue,
)


# ========================================================
# AnalogWaveform to DoubleAnalogWaveform
# ========================================================
def test___default_float64_complex_waveform___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform(0, np.complex128)

    dbl_analog_waveform = float64_complex_waveform_to_protobuf(analog_waveform)

    assert not dbl_analog_waveform.attributes
    assert dbl_analog_waveform.dt == 0
    assert not dbl_analog_waveform.HasField("t0")
    assert list(dbl_analog_waveform.y_data) == []


def test___float64_complex_waveform_samples_only___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform(2, np.complex128)

    dbl_analog_waveform = float64_complex_waveform_to_protobuf(analog_waveform)

    # Interleaved real/imaginary data.
    assert list(dbl_analog_waveform.y_data) == [0.0, 0.0, 0.0, 0.0]


def test___float64_complex_waveform_non_zero_samples___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)

    dbl_analog_waveform = float64_complex_waveform_to_protobuf(analog_waveform)

    assert list(dbl_analog_waveform.y_data) == [1.5, 2.5, 3.5, 4.5]


def test___float64_complex_waveform_with_extended_properties___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform(0, np.complex128)
    analog_waveform.channel_name = "Dev1/ai0"
    analog_waveform.unit_description = "Volts"

    dbl_analog_waveform = float64_complex_waveform_to_protobuf(analog_waveform)

    assert dbl_analog_waveform.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert dbl_analog_waveform.attributes["NI_UnitDescription"].string_value == "Volts"


def test___float64_complex_waveform_with_standard_timing___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    dbl_analog_waveform = float64_complex_waveform_to_protobuf(analog_waveform)

    assert dbl_analog_waveform.dt == 1.0
    bin_dt = DateTime(t0_dt)
    converted_t0 = bintime_datetime_to_protobuf(bin_dt)
    assert dbl_analog_waveform.t0 == converted_t0


# ========================================================
# DoubleAnalogWaveform to AnalogWaveform
# ========================================================
def test___default_dbl_complex_wfm___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleComplexWaveform()

    analog_waveform = float64_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert not analog_waveform.extended_properties
    assert analog_waveform.timing == Timing.empty
    assert analog_waveform.scaled_data.size == 0
    assert analog_waveform.scale_mode == NoneScaleMode()


def test___dbl_complex_wfm_with_y_data___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleComplexWaveform(y_data=[1.0, 2.0, 3.0, 4.0])

    analog_waveform = float64_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert list(analog_waveform.scaled_data) == [1.0 + 2.0j, 3.0 + 4.0j]


def test___dbl_complex_wfm_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    dbl_analog_wfm = DoubleComplexWaveform(attributes=attributes)

    analog_waveform = float64_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.channel_name == "Dev1/ai0"
    assert analog_waveform.unit_description == "Volts"


def test___dbl_complex_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleComplexWaveform(t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0])

    analog_waveform = float64_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_complex_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleComplexWaveform(dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0])

    analog_waveform = float64_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_complex_wfm_with_timing_no_dt___convert___valid_python_object() -> None:
    t0_dt = DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleComplexWaveform(t0=t0_pt, y_data=[1.0, 2.0, 3.0, 4.0])

    analog_waveform = float64_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert not analog_waveform.timing.has_sample_interval
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE


# =================================================================================

# ========================================================
# AnalogWaveform to DoubleAnalogWaveform
# ========================================================
def test___default_int16_complex_waveform___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform(0, ComplexInt32DType)

    dbl_analog_waveform = int16_complex_waveform_to_protobuf(analog_waveform)

    assert not dbl_analog_waveform.attributes
    assert dbl_analog_waveform.dt == 0
    assert not dbl_analog_waveform.HasField("t0")
    assert list(dbl_analog_waveform.y_data) == []


def test___int16_complex_waveform_samples_only___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform(2, ComplexInt32DType)

    dbl_analog_waveform = int16_complex_waveform_to_protobuf(analog_waveform)

    # Interleaved real/imaginary data.
    assert list(dbl_analog_waveform.y_data) == [0, 0, 0, 0]


def test___int16_complex_waveform_non_zero_samples___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)

    dbl_analog_waveform = int16_complex_waveform_to_protobuf(analog_waveform)

    assert list(dbl_analog_waveform.y_data) == [1, 2, 3, 4]


def test___int16_complex_waveform_with_extended_properties___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform(0, ComplexInt32DType)
    analog_waveform.channel_name = "Dev1/ai0"
    analog_waveform.unit_description = "Volts"

    dbl_analog_waveform = int16_complex_waveform_to_protobuf(analog_waveform)

    assert dbl_analog_waveform.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert dbl_analog_waveform.attributes["NI_UnitDescription"].string_value == "Volts"


def test___int16_complex_waveform_with_standard_timing___convert___valid_protobuf() -> None:
    analog_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    dbl_analog_waveform = int16_complex_waveform_to_protobuf(analog_waveform)

    assert dbl_analog_waveform.dt == 1.0
    bin_dt = DateTime(t0_dt)
    converted_t0 = bintime_datetime_to_protobuf(bin_dt)
    assert dbl_analog_waveform.t0 == converted_t0


# ========================================================
# DoubleAnalogWaveform to AnalogWaveform
# ========================================================
def test___default_int16_complex_wfm___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleComplexWaveform()

    analog_waveform = int16_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert not analog_waveform.extended_properties
    assert analog_waveform.timing == Timing.empty
    assert analog_waveform.scaled_data.size == 0
    assert analog_waveform.scale_mode == NoneScaleMode()


def test___int16_complex_wfm_with_y_data___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleComplexWaveform(y_data=[1, 2, 3, 4])

    analog_waveform = int16_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert list(analog_waveform.scaled_data) == [1 + 2j, 3 + 4j]


def test___int16_complex_wfm_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    dbl_analog_wfm = DoubleComplexWaveform(attributes=attributes)

    analog_waveform = int16_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.channel_name == "Dev1/ai0"
    assert analog_waveform.unit_description == "Volts"


def test___int16_complex_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleComplexWaveform(t0=t0_pt, dt=0.1, y_data=[1, 2, 3, 4])

    analog_waveform = int16_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___int16_complex_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleComplexWaveform(dt=0.1, y_data=[1, 2, 3, 4])

    analog_waveform = int16_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___int16_complex_wfm_with_timing_no_dt___convert___valid_python_object() -> None:
    t0_dt = DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleComplexWaveform(t0=t0_pt, y_data=[1, 2, 3, 4])

    analog_waveform = int16_complex_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert not analog_waveform.timing.has_sample_interval
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE
