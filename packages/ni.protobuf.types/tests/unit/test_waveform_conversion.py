import datetime as dt
from typing import Any

import nitypes.bintime as bt
import numpy as np
import pytest
from nitypes.complex import ComplexInt32DType
from nitypes.time import convert_datetime
from nitypes.waveform import (
    AnalogWaveform,
    ComplexWaveform,
    DigitalWaveform,
    LinearScaleMode,
    NoneScaleMode,
    SampleIntervalMode,
    Spectrum,
    Timing,
)

from ni.protobuf.types.precision_timestamp_conversion import (
    bintime_datetime_to_protobuf,
)
from ni.protobuf.types.precision_timestamp_pb2 import PrecisionTimestamp
from ni.protobuf.types.waveform_conversion import (
    digital_waveform_from_protobuf,
    digital_waveform_to_protobuf,
    float64_analog_waveform_from_protobuf,
    float64_analog_waveform_to_protobuf,
    float64_complex_waveform_from_protobuf,
    float64_complex_waveform_to_protobuf,
    float64_spectrum_from_protobuf,
    float64_spectrum_to_protobuf,
    int16_analog_waveform_from_protobuf,
    int16_analog_waveform_to_protobuf,
    int16_complex_waveform_from_protobuf,
    int16_complex_waveform_to_protobuf,
)
from ni.protobuf.types.waveform_pb2 import (
    DigitalWaveform as DigitalWaveformProto,
    DoubleAnalogWaveform,
    DoubleComplexWaveform,
    DoubleSpectrum,
    I16AnalogWaveform,
    I16ComplexWaveform,
    LinearScale,
    Scale,
    WaveformAttributeValue,
)


# ========================================================
# AnalogWaveform to DoubleAnalogWaveform
# ========================================================
def test___default_analog_waveform___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform()

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

    assert not dbl_analog_waveform.attributes
    assert dbl_analog_waveform.dt == 0
    assert not dbl_analog_waveform.HasField("t0")
    assert list(dbl_analog_waveform.y_data) == []


def test___analog_waveform_samples_only___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform(5)

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

    assert list(dbl_analog_waveform.y_data) == [0.0, 0.0, 0.0, 0.0, 0.0]


def test___analog_waveform_non_zero_samples___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1.0, 2.0, 3.0]))

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

    assert list(dbl_analog_waveform.y_data) == [1.0, 2.0, 3.0]


def test___analog_waveform_with_extended_properties___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform()
    analog_waveform.channel_name = "Dev1/ai0"
    analog_waveform.units = "Volts"

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

    assert dbl_analog_waveform.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert dbl_analog_waveform.attributes["NI_UnitDescription"].string_value == "Volts"


def test___analog_waveform_with_standard_timing___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1.0, 2.0, 3.0]))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

    _assert_proto_standard_timing(dbl_analog_waveform, t0_dt)


def test___analog_waveform_with_standard_timing_and_offset___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1.0, 2.0, 3.0]))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

    _assert_proto_standard_timing_with_offset(dbl_analog_waveform, t0_dt, time_offset)


def test___analog_waveform_with_standard_timing___round_trip___waveforms_match() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1.0, 2.0, 3.0]))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)
    converted_analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_waveform)

    assert analog_waveform == converted_analog_waveform


def test___analog_waveform_with_none_timing___round_trip___waveforms_match() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1.0, 2.0, 3.0]))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    time_offset = dt.timedelta(milliseconds=1000)
    analog_waveform.timing = Timing.create_with_no_interval(
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)
    converted_analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_waveform)

    assert analog_waveform == converted_analog_waveform


def test___analog_waveform_with_irregular_timing___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1.0, 2.0, 3.0]))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    timestamps = [
        t0_dt,
        t0_dt + dt.timedelta(milliseconds=1000),
        t0_dt + dt.timedelta(milliseconds=3000),
    ]
    analog_waveform.timing = Timing.create_with_irregular_interval(timestamps)

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

    assert list(dbl_analog_waveform.timestamps) == _to_proto_timestamps(timestamps)


# ========================================================
# DoubleAnalogWaveform to AnalogWaveform
# ========================================================
def test___default_dbl_analog_wfm___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleAnalogWaveform()

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert not analog_waveform.extended_properties
    assert analog_waveform.timing == Timing.empty
    assert analog_waveform.scaled_data.size == 0
    assert analog_waveform.scale_mode == NoneScaleMode()


def test___dbl_analog_wfm_with_y_data___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleAnalogWaveform(y_data=[1.0, 2.0, 3.0])

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert list(analog_waveform.scaled_data) == [1.0, 2.0, 3.0]


def test___dbl_analog_wfm_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    dbl_analog_wfm = DoubleAnalogWaveform(attributes=attributes)

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.channel_name == "Dev1/ai0"
    assert analog_waveform.units == "Volts"


def test___dbl_analog_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleAnalogWaveform(t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0])

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_analog_wfm_with_timing___round_trip___waveforms_match() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleAnalogWaveform(
        t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0], timestamp=t0_pt, time_offset=0.0
    )

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)
    converted_dbl_analog_wfm = float64_analog_waveform_to_protobuf(analog_waveform)

    assert dbl_analog_wfm == converted_dbl_analog_wfm


def test___dbl_analog_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleAnalogWaveform(dt=0.1, y_data=[1.0, 2.0, 3.0])

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    # assert analog_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
    assert not analog_waveform.timing.has_start_time
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_analog_wfm_with_timing_no_dt___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleAnalogWaveform(t0=t0_pt, y_data=[1.0, 2.0, 3.0])

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert not analog_waveform.timing.has_sample_interval
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE


def test___dbl_analog_wfm_with_dt_and_offset___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleAnalogWaveform(dt=0.1, y_data=[1.0, 2.0, 3.0], time_offset=1.0)

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert not analog_waveform.timing.has_timestamp
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.time_offset == bt.TimeDelta(1.0)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_analog_wfm_with_t0_and_timestamp_and_offset___convert___valid_python_object() -> (
    None
):
    sample_interval = 0.1
    t0_seconds = 1000001
    t0_pt = PrecisionTimestamp(seconds=t0_seconds, fractional_seconds=0)
    timestamp_seconds = 1000000
    timestamp_pt = PrecisionTimestamp(seconds=timestamp_seconds, fractional_seconds=0)
    time_offset = 1.0
    dbl_analog_wfm = DoubleAnalogWaveform(
        t0=t0_pt,
        dt=0.1,
        y_data=[1.0, 2.0, 3.0],
        timestamp=timestamp_pt,
        time_offset=time_offset,
    )

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    _assert_waveform_timestamp_and_t0_timing(
        analog_waveform, t0_seconds, timestamp_seconds, sample_interval, time_offset
    )


def test___dbl_analog_wfm_with_t0_and_offset_no_timestamp___convert___raises_exception() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleAnalogWaveform(t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0], time_offset=1.0)

    with pytest.raises(AttributeError):
        _ = float64_analog_waveform_from_protobuf(dbl_analog_wfm)


# ========================================================
# ComplexWaveform to DoubleComplexWaveform
# ========================================================
def test___default_float64_complex_waveform___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform(0, np.complex128)

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

    assert not dbl_complex_waveform.attributes
    assert dbl_complex_waveform.dt == 0
    assert not dbl_complex_waveform.HasField("t0")
    assert list(dbl_complex_waveform.y_data) == []


def test___float64_complex_waveform_samples_only___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform(2, np.complex128)

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

    # Interleaved real/imaginary data.
    assert list(dbl_complex_waveform.y_data) == [0.0, 0.0, 0.0, 0.0]


def test___float64_complex_waveform_non_zero_samples___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

    assert list(dbl_complex_waveform.y_data) == [1.5, 2.5, 3.5, 4.5]


def test___float64_complex_waveform_with_extended_properties___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform(0, np.complex128)
    complex_waveform.channel_name = "Dev1/ai0"
    complex_waveform.units = "Volts"

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

    assert dbl_complex_waveform.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert dbl_complex_waveform.attributes["NI_UnitDescription"].string_value == "Volts"


def test___float64_complex_waveform_with_standard_timing___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    complex_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

    _assert_proto_standard_timing(dbl_complex_waveform, t0_dt)


def test___float64_complex_waveform_with_standard_timing_and_offset___convert___valid_protobuf() -> (
    None
):
    complex_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    complex_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

    _assert_proto_standard_timing_with_offset(dbl_complex_waveform, t0_dt, time_offset)


def test___float64_complex_waveform_with_standard_timing_and_offset___round_trip___waveforms_match() -> (
    None
):
    complex_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    complex_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)
    converted_complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert complex_waveform == converted_complex_waveform


def test___float64_complex_waveform_with_none_timing___round_trip___waveforms_match() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    time_offset = dt.timedelta(milliseconds=1000)
    complex_waveform.timing = Timing.create_with_no_interval(
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)
    converted_complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert complex_waveform == converted_complex_waveform


def test___float64_complex_waveform_with_irregular_timing___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    timestamps = [t0_dt, t0_dt + dt.timedelta(milliseconds=1000)]
    complex_waveform.timing = Timing.create_with_irregular_interval(timestamps)

    dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

    assert list(dbl_complex_waveform.timestamps) == _to_proto_timestamps(timestamps)


# ========================================================
# DoubleComplexWaveform to ComplexWaveform
# ========================================================
def test___default_dbl_complex_wfm___convert___valid_python_object() -> None:
    dbl_complex_waveform = DoubleComplexWaveform()

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert not complex_waveform.extended_properties
    assert complex_waveform.timing == Timing.empty
    assert complex_waveform.scaled_data.size == 0
    assert complex_waveform.scale_mode == NoneScaleMode()


def test___dbl_complex_wfm_with_y_data___convert___valid_python_object() -> None:
    dbl_complex_waveform = DoubleComplexWaveform(y_data=[1.0, 2.0, 3.0, 4.0])

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert list(complex_waveform.scaled_data) == [1.0 + 2.0j, 3.0 + 4.0j]


def test___dbl_complex_wfm_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    dbl_complex_waveform = DoubleComplexWaveform(attributes=attributes)

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert complex_waveform.channel_name == "Dev1/ai0"
    assert complex_waveform.units == "Volts"


def test___dbl_complex_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_complex_waveform = DoubleComplexWaveform(t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0])

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert complex_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert complex_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_complex_wfm_with_timing___round_trip___waveforms_match() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_complex_waveform = DoubleComplexWaveform(
        t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0], timestamp=t0_pt, time_offset=0.0
    )

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)
    converted_dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

    assert dbl_complex_waveform == converted_dbl_complex_waveform


def test___dbl_complex_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    dbl_complex_waveform = DoubleComplexWaveform(dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0])

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    # assert complex_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
    assert not complex_waveform.timing.has_start_time
    assert complex_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_complex_wfm_with_timing_no_dt___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_complex_waveform = DoubleComplexWaveform(t0=t0_pt, y_data=[1.0, 2.0, 3.0, 4.0])

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert complex_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert not complex_waveform.timing.has_sample_interval
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE


def test___dbl_complex_wfm_with_dt_and_offset___convert___valid_python_object() -> None:
    dbl_complex_waveform = DoubleComplexWaveform(
        dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0], time_offset=1.0
    )

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert not complex_waveform.timing.has_timestamp
    assert complex_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert complex_waveform.timing.time_offset == bt.TimeDelta(1.0)
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_complex_wfm_with_t0_and_timestamp_and_offset___convert___valid_python_object() -> (
    None
):
    sample_interval = 0.1
    t0_seconds = 1000001
    t0_pt = PrecisionTimestamp(seconds=t0_seconds, fractional_seconds=0)
    timestamp_seconds = 1000000
    timestamp_pt = PrecisionTimestamp(seconds=timestamp_seconds, fractional_seconds=0)
    time_offset = 1.0
    dbl_complex_waveform = DoubleComplexWaveform(
        t0=t0_pt,
        dt=0.1,
        y_data=[1.0, 2.0, 3.0, 4.0],
        timestamp=timestamp_pt,
        time_offset=time_offset,
    )

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    _assert_waveform_timestamp_and_t0_timing(
        complex_waveform, t0_seconds, timestamp_seconds, sample_interval, time_offset
    )


def test___dbl_complex_wfm_with_t0_and_offset_no_timestamp___convert___raises_exception() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_complex_waveform = DoubleComplexWaveform(
        t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0], time_offset=1.0
    )

    with pytest.raises(AttributeError):
        _ = float64_complex_waveform_from_protobuf(dbl_complex_waveform)


# ========================================================
# ComplexWaveform to I16ComplexWaveform
# ========================================================
def test___default_int16_complex_waveform___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform(0, ComplexInt32DType)

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    assert not i16_complex_waveform.attributes
    assert i16_complex_waveform.dt == 0
    assert not i16_complex_waveform.HasField("t0")
    assert not i16_complex_waveform.HasField("scale")
    assert list(i16_complex_waveform.y_data) == []


def test___int16_complex_waveform_samples_only___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform(2, ComplexInt32DType)

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    # Interleaved real/imaginary data.
    assert list(i16_complex_waveform.y_data) == [0, 0, 0, 0]


def test___int16_complex_waveform_non_zero_samples___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    assert list(i16_complex_waveform.y_data) == [1, 2, 3, 4]


def test___int16_complex_waveform_with_extended_properties___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform(0, ComplexInt32DType)
    complex_waveform.channel_name = "Dev1/ai0"
    complex_waveform.units = "Volts"

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    assert i16_complex_waveform.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert i16_complex_waveform.attributes["NI_UnitDescription"].string_value == "Volts"


def test___int16_complex_waveform_with_standard_timing___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    complex_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    _assert_proto_standard_timing(i16_complex_waveform, t0_dt)


def test___int16_complex_waveform_with_standard_timing_and_offset___convert___valid_protobuf() -> (
    None
):
    complex_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    complex_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    _assert_proto_standard_timing_with_offset(i16_complex_waveform, t0_dt, time_offset)


def test___int16_complex_waveform_with_standard_timing_and_offset___round_trip___waveforms_match() -> (
    None
):
    complex_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    complex_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)
    converted_complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert complex_waveform == converted_complex_waveform


def test___int16_complex_waveform_with_none_timing___round_trip___waveforms_match() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    time_offset = dt.timedelta(milliseconds=1000)
    complex_waveform.timing = Timing.create_with_no_interval(
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)
    converted_complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert complex_waveform == converted_complex_waveform


def test___int16_complex_waveform_with_irregular_timing___convert___valid_protobuf() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    timestamps = [t0_dt, t0_dt + dt.timedelta(milliseconds=1000)]
    complex_waveform.timing = Timing.create_with_irregular_interval(timestamps)

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    assert list(i16_complex_waveform.timestamps) == _to_proto_timestamps(timestamps)


def test___int16_complex_waveform_with_scaling___convert___valid_protobuf() -> None:
    scale_mode = LinearScaleMode(2.0, 3.0)
    complex_waveform = ComplexWaveform.from_array_1d(
        [(1, 2), (3, 4)],
        ComplexInt32DType,
        scale_mode=scale_mode,
    )

    i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    assert i16_complex_waveform.scale.linear_scale.gain == 2.0
    assert i16_complex_waveform.scale.linear_scale.offset == 3.0


# ========================================================
# I16ComplexWaveform to ComplexWaveform
# ========================================================
def test___default_int16_complex_wfm___convert___valid_python_object() -> None:
    i16_complex_waveform = I16ComplexWaveform()

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert not complex_waveform.extended_properties
    assert complex_waveform.timing == Timing.empty
    assert complex_waveform.scaled_data.size == 0
    assert complex_waveform.scale_mode == NoneScaleMode()


def test___int16_complex_wfm_with_y_data___convert___valid_python_object() -> None:
    i16_complex_waveform = I16ComplexWaveform(y_data=[1, 2, 3, 4])

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    expected_raw_data = np.array([(1, 2), (3, 4)], ComplexInt32DType)
    assert np.array_equal(complex_waveform.raw_data, expected_raw_data)


def test___int16_complex_wfm_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    i16_complex_waveform = I16ComplexWaveform(attributes=attributes)

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert complex_waveform.channel_name == "Dev1/ai0"
    assert complex_waveform.units == "Volts"


def test___int16_complex_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_complex_waveform = I16ComplexWaveform(t0=t0_pt, dt=0.1, y_data=[1, 2, 3, 4])

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert complex_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert complex_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___int16_complex_wfm_with_timing___round_trip___waveforms_valid() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_complex_waveform = I16ComplexWaveform(
        t0=t0_pt, dt=0.1, y_data=[1, 2, 3, 4], timestamp=t0_pt, time_offset=0.0
    )

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)
    converted_i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

    assert i16_complex_waveform == converted_i16_complex_waveform


def test___int16_complex_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    i16_complex_waveform = I16ComplexWaveform(dt=0.1, y_data=[1, 2, 3, 4])

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    # assert complex_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
    assert not complex_waveform.timing.has_start_time
    assert complex_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___int16_complex_wfm_with_timing_no_dt___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_complex_waveform = I16ComplexWaveform(t0=t0_pt, y_data=[1, 2, 3, 4])

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert complex_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert not complex_waveform.timing.has_sample_interval
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE


def test___int16_complex_wfm_with_scaling___convert___valid_python_object() -> None:
    linear_scale = LinearScale(gain=2.0, offset=3.0)
    scale = Scale(linear_scale=linear_scale)
    i16_complex_waveform = I16ComplexWaveform(y_data=[1, 2, 3, 4], scale=scale)

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert isinstance(complex_waveform.scale_mode, LinearScaleMode)
    assert complex_waveform.scale_mode.gain == 2.0
    assert complex_waveform.scale_mode.offset == 3.0


def test___int16_complex_wfm_with_t0_and_timestamp_and_offset___convert___valid_python_object() -> (
    None
):
    sample_interval = 0.1
    t0_seconds = 1000001
    t0_pt = PrecisionTimestamp(seconds=t0_seconds, fractional_seconds=0)
    timestamp_seconds = 1000000
    timestamp_pt = PrecisionTimestamp(seconds=timestamp_seconds, fractional_seconds=0)
    time_offset = 1.0
    i16_complex_waveform = I16ComplexWaveform(
        t0=t0_pt,
        dt=sample_interval,
        y_data=[1, 2, 3, 4],
        timestamp=timestamp_pt,
        time_offset=time_offset,
    )

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    _assert_waveform_timestamp_and_t0_timing(
        complex_waveform, t0_seconds, timestamp_seconds, sample_interval, time_offset
    )


def test___int16_complex_wfm_with_t0_and_offset_no_timestamp___convert___raises_exception() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_complex_waveform = I16ComplexWaveform(
        t0=t0_pt, dt=0.1, y_data=[1, 2, 3, 4], time_offset=1.0
    )

    with pytest.raises(AttributeError):
        _ = int16_complex_waveform_from_protobuf(i16_complex_waveform)


# ========================================================
# AnalogWaveform to I16AnalogWaveform
# ========================================================
def test___default_int16_analog_waveform___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform(0, np.int16)

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

    assert not i16_analog_waveform.attributes
    assert i16_analog_waveform.dt == 0
    assert not i16_analog_waveform.HasField("t0")
    assert not i16_analog_waveform.HasField("scale")
    assert list(i16_analog_waveform.y_data) == []


def test___int16_analog_waveform_samples_only___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform(5, np.int16)

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

    assert list(i16_analog_waveform.y_data) == [0, 0, 0, 0, 0]


def test___int16_analog_waveform_non_zero_samples___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1, 2, 3], dtype=np.int16))

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

    assert list(i16_analog_waveform.y_data) == [1, 2, 3]


def test___int16_analog_waveform_with_extended_properties___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform(0, np.int16)
    analog_waveform.channel_name = "Dev1/ai0"
    analog_waveform.units = "Volts"

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

    assert i16_analog_waveform.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert i16_analog_waveform.attributes["NI_UnitDescription"].string_value == "Volts"


def test___int16_analog_waveform_with_standard_timing___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1, 2, 3], dtype=np.int16))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

    _assert_proto_standard_timing(i16_analog_waveform, t0_dt)


def test___int16_analog_waveform_with_standard_timing_and_offset___convert___valid_protobuf() -> (
    None
):
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1, 2, 3], dtype=np.int16))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

    _assert_proto_standard_timing_with_offset(i16_analog_waveform, t0_dt, time_offset)


def test___int16_analog_waveform_with_standard_timing_and_offset___round_trip___waveforms_match() -> (
    None
):
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1, 2, 3], dtype=np.int16))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)
    converted_analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_waveform)

    assert analog_waveform == converted_analog_waveform


def test___int16_analog_waveform_with_none_timing___round_trip___waveforms_match() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1, 2, 3], dtype=np.int16))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    time_offset = dt.timedelta(milliseconds=1000)
    analog_waveform.timing = Timing.create_with_no_interval(
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)
    converted_analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_waveform)

    assert analog_waveform == converted_analog_waveform


def test___int16_analog_waveform_with_irregular_timing___convert___valid_protobuf() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1, 2, 3], dtype=np.int16))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    timestamps = [
        t0_dt,
        t0_dt + dt.timedelta(milliseconds=1000),
        t0_dt + dt.timedelta(milliseconds=3000),
    ]
    analog_waveform.timing = Timing.create_with_irregular_interval(timestamps)

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

    assert list(i16_analog_waveform.timestamps) == _to_proto_timestamps(timestamps)


def test___int16_analog_waveform_with_scaling___convert___valid_protobuf() -> None:
    scale_mode = LinearScaleMode(2.0, 3.0)
    analog_waveform = AnalogWaveform.from_array_1d(
        np.array([1, 2, 3], dtype=np.int16),
        scale_mode=scale_mode,
    )

    i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

    assert i16_analog_waveform.scale.linear_scale.gain == 2.0
    assert i16_analog_waveform.scale.linear_scale.offset == 3.0


# ========================================================
# I16AnalogWaveform to AnalogWaveform
# ========================================================
def test___default_i16_analog_wfm___convert___valid_python_object() -> None:
    i16_analog_wfm = I16AnalogWaveform()

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    assert not analog_waveform.extended_properties
    assert analog_waveform.timing == Timing.empty
    assert analog_waveform.scaled_data.size == 0
    assert analog_waveform.scale_mode == NoneScaleMode()


def test___i16_analog_wfm_with_y_data___convert___valid_python_object() -> None:
    i16_analog_wfm = I16AnalogWaveform(y_data=[1, 2, 3])

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    expected_raw_data = np.array([1, 2, 3], dtype=np.int16)
    assert np.array_equal(analog_waveform.raw_data, expected_raw_data)


def test___i16_analog_wfm_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    i16_analog_wfm = I16AnalogWaveform(attributes=attributes)

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    assert analog_waveform.channel_name == "Dev1/ai0"
    assert analog_waveform.units == "Volts"


def test___i16_analog_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_analog_wfm = I16AnalogWaveform(t0=t0_pt, dt=0.1, y_data=[1, 2, 3])

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___i16_analog_wfm_with_timing___round_trip___waveforms_match() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_analog_wfm = I16AnalogWaveform(
        t0=t0_pt, dt=0.1, y_data=[1, 2, 3], timestamp=t0_pt, time_offset=0.0
    )

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)
    converted_i16_analog_wfm = int16_analog_waveform_to_protobuf(analog_waveform)

    assert i16_analog_wfm == converted_i16_analog_wfm


def test___i16_analog_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    i16_analog_wfm = I16AnalogWaveform(dt=0.1, y_data=[1, 2, 3])

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    # assert analog_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
    assert not analog_waveform.timing.has_start_time
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___i16_analog_wfm_with_timing_no_dt___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_analog_wfm = I16AnalogWaveform(t0=t0_pt, y_data=[1, 2, 3])

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert not analog_waveform.timing.has_sample_interval
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE


def test___i16_analog_wfm_with_scaling___convert___valid_python_object() -> None:
    linear_scale = LinearScale(gain=2.0, offset=3.0)
    scale = Scale(linear_scale=linear_scale)
    i16_analog_wfm = I16AnalogWaveform(y_data=[1, 2, 3], scale=scale)

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    assert isinstance(analog_waveform.scale_mode, LinearScaleMode)
    assert analog_waveform.scale_mode.gain == 2.0
    assert analog_waveform.scale_mode.offset == 3.0


def test___i16_analog_wfm_with_dt_and_offset___convert___valid_python_object() -> None:
    i16_analog_wfm = I16AnalogWaveform(dt=0.1, y_data=[1, 2, 3], time_offset=1.0)

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    assert not analog_waveform.timing.has_timestamp
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.time_offset == bt.TimeDelta(1.0)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___i16_analog_wfm_with_t0_and_offet_no_timestamp___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_analog_wfm = I16AnalogWaveform(t0=t0_pt, dt=0.1, y_data=[1, 2, 3], time_offset=1.0)

    with pytest.raises(AttributeError):
        _ = int16_analog_waveform_from_protobuf(i16_analog_wfm)


# ========================================================
# Spectrum to DoubleSpectrum
# ========================================================
def test___default_spectrum___convert___valid_protobuf() -> None:
    spectrum = Spectrum()

    dbl_spectrum = float64_spectrum_to_protobuf(spectrum)

    assert not dbl_spectrum.attributes
    assert spectrum.start_frequency == 0.0
    assert spectrum.frequency_increment == 0.0
    assert list(dbl_spectrum.data) == []


def test___spectrum_with_data___convert___valid_protobuf() -> None:
    spectrum = Spectrum.from_array_1d(np.array([1.0, 2.0, 3.0]))
    spectrum.start_frequency = 100.0
    spectrum.frequency_increment = 10.0

    dbl_spectrum = float64_spectrum_to_protobuf(spectrum)

    assert list(dbl_spectrum.data) == [1.0, 2.0, 3.0]
    assert dbl_spectrum.start_frequency == 100.0
    assert dbl_spectrum.frequency_increment == 10.0


def test___spectrum_with_extended_properties___convert___valid_protobuf() -> None:
    spectrum = Spectrum()
    spectrum.channel_name = "Dev1/ai0"
    spectrum.units = "Volts"

    dbl_spectrum = float64_spectrum_to_protobuf(spectrum)

    assert dbl_spectrum.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert dbl_spectrum.attributes["NI_UnitDescription"].string_value == "Volts"


# ========================================================
# DoubleSpectrum to Spectrum
# ========================================================
def test___default_dbl_spectrum___convert___valid_python_object() -> None:
    dbl_spectrum = DoubleSpectrum()

    spectrum = float64_spectrum_from_protobuf(dbl_spectrum)

    assert not spectrum.extended_properties
    assert spectrum.start_frequency == 0.0
    assert spectrum.frequency_increment == 0.0
    assert spectrum.sample_count == 0
    assert spectrum.data.size == 0


def test___dbl_spectrum_with_data___convert___valid_python_object() -> None:
    dbl_spectrum = DoubleSpectrum(
        data=[1.0, 2.0, 3.0], start_frequency=100.0, frequency_increment=10.0
    )

    spectrum = float64_spectrum_from_protobuf(dbl_spectrum)

    assert list(spectrum.data) == [1.0, 2.0, 3.0]
    assert spectrum.start_frequency == 100.0
    assert spectrum.frequency_increment == 10.0


def test___dbl_spectrum_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    dbl_spectrum = DoubleSpectrum(attributes=attributes)

    spectrum = float64_spectrum_from_protobuf(dbl_spectrum)

    assert spectrum.channel_name == "Dev1/ai0"
    assert spectrum.units == "Volts"


# ========================================================
# DigitalWaveform to protobuf
# ========================================================
def test___default_digital_waveform___convert___valid_protobuf() -> None:
    digital_waveform = DigitalWaveform()

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    assert not digital_waveform_proto.attributes
    assert digital_waveform_proto.dt == 0
    assert not digital_waveform_proto.HasField("t0")
    assert digital_waveform_proto.y_data == b""
    assert digital_waveform_proto.signal_count == 1


def test___digital_waveform_with_data___convert___valid_protobuf() -> None:
    data = np.array([[0, 1, 3], [7, 5, 1]], dtype=np.uint8)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    assert digital_waveform_proto.y_data == b"\x00\x01\x03\x07\x05\x01"
    assert digital_waveform_proto.signal_count == 3


def test___digital_waveform_with_extended_properties___convert___valid_protobuf() -> None:
    digital_waveform = DigitalWaveform()
    digital_waveform.channel_name = "Dev1/port0"

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    assert digital_waveform_proto.attributes["NI_ChannelName"].string_value == "Dev1/port0"


def test___digital_waveform_with_standard_timing___convert___valid_protobuf() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.bool)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    digital_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    _assert_proto_standard_timing(digital_waveform_proto, t0_dt)
    assert digital_waveform_proto.signal_count == 3


def test___digital_waveform_with_standard_timing_and_offset___convert___valid_protobuf() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.bool)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    digital_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    _assert_proto_standard_timing_with_offset(digital_waveform_proto, t0_dt, time_offset)
    assert digital_waveform_proto.signal_count == 3


def test___digital_waveform_with_standard_timing_and_offset___round_trip___timings_match() -> None:
    # Has to be created as uint8 since from_protobuf assumes that type.
    data = np.array([[7, 1, 4], [1, 0, 1]], dtype=np.uint8)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    sample_interval = dt.timedelta(milliseconds=1000)
    time_offset = dt.timedelta(milliseconds=1000)
    digital_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=sample_interval,
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)
    converted_digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert digital_waveform == converted_digital_waveform


def test___digital_waveform_with_none_timing___round_trip___timings_match() -> None:
    # Has to be created as uint8 since from_protobuf assumes that type.
    data = np.array([[7, 1, 4], [1, 0, 1]], dtype=np.uint8)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    time_offset = dt.timedelta(milliseconds=1000)
    digital_waveform.timing = Timing.create_with_no_interval(
        timestamp=t0_dt,
        time_offset=time_offset,
    )

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)
    converted_digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert digital_waveform == converted_digital_waveform


def test___digital_waveform_with_irregular_timing___convert___raises_value_error() -> None:
    data = np.array([[7, 1, 4], [1, 0, 1]], dtype=np.uint8)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    timestamps = [t0_dt, t0_dt + dt.timedelta(milliseconds=1000)]
    digital_waveform.timing = Timing.create_with_irregular_interval(timestamps)

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    assert list(digital_waveform_proto.timestamps) == _to_proto_timestamps(timestamps)


# ========================================================
# DigitalWaveform from protobuf
# ========================================================
def test___default_digital_waveform_proto___convert___valid_python_object() -> None:
    digital_waveform_proto = DigitalWaveformProto(signal_count=1)

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert not digital_waveform.extended_properties
    assert digital_waveform.timing == Timing.empty
    assert digital_waveform.data.size == 0
    assert digital_waveform.signal_count == 1


def test___digital_waveform_proto_with_data___convert___valid_python_object() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    digital_waveform_proto = DigitalWaveformProto(y_data=data.tobytes(), signal_count=3)

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert np.array_equal(digital_waveform.data, data)
    assert digital_waveform.signal_count == 3


def test___digital_waveform_proto_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/port0"),
    }
    digital_waveform_proto = DigitalWaveformProto(attributes=attributes, signal_count=1)

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert digital_waveform.channel_name == "Dev1/port0"


def test___digital_waveform_proto_with_timing___convert___valid_python_object() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    digital_waveform_proto = DigitalWaveformProto(
        t0=t0_pt, dt=0.1, y_data=data.tobytes(), signal_count=3
    )

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert digital_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert digital_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert digital_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___digital_waveform_proto_with_timing___round_trip___waveforms_match() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    digital_waveform_proto = DigitalWaveformProto(
        t0=t0_pt, dt=0.1, y_data=data.tobytes(), timestamp=t0_pt, time_offset=0.0, signal_count=3
    )

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)
    converted_digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    assert digital_waveform_proto == converted_digital_waveform_proto


def test___digital_waveform_proto_with_timing_no_t0___convert___valid_python_object() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    digital_waveform_proto = DigitalWaveformProto(dt=0.1, y_data=data.tobytes(), signal_count=3)

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    # assert digital_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
    assert not digital_waveform.timing.has_start_time
    assert digital_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert digital_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___digital_waveform_proto_with_timing_no_dt___convert___valid_python_object() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    digital_waveform_proto = DigitalWaveformProto(t0=t0_pt, y_data=data.tobytes(), signal_count=3)

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert digital_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert not digital_waveform.timing.has_sample_interval
    assert digital_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE


def test___digital_waveform_proto_with_dt_and_offset___convert___valid_python_object() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    digital_waveform_proto = DigitalWaveformProto(
        dt=0.1, y_data=data.tobytes(), time_offset=1.0, signal_count=3
    )

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert not digital_waveform.timing.has_timestamp
    assert digital_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert digital_waveform.timing.time_offset == bt.TimeDelta(1.0)
    assert digital_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___digital_waveform_proto_with_t0_and_timestamp_and_offset___convert___valid_python_object() -> (
    None
):
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    sample_interval = 0.1
    t0_seconds = 1000001
    t0_pt = PrecisionTimestamp(seconds=t0_seconds, fractional_seconds=0)
    timestamp_seconds = 1000000
    timestamp_pt = PrecisionTimestamp(seconds=timestamp_seconds, fractional_seconds=0)
    time_offset = 1.0
    digital_waveform_proto = DigitalWaveformProto(
        t0=t0_pt,
        dt=sample_interval,
        signal_count=3,
        y_data=data.tobytes(),
        timestamp=timestamp_pt,
        time_offset=time_offset,
    )

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    _assert_waveform_timestamp_and_t0_timing(
        digital_waveform, t0_seconds, timestamp_seconds, sample_interval, time_offset
    )


def test___digital_waveform_proto_with_t0_and_offset_no_timestamp___convert___raises_exception() -> (
    None
):
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    digital_waveform_proto = DigitalWaveformProto(
        t0=t0_pt, dt=0.1, y_data=data.tobytes(), time_offset=1.0, signal_count=3
    )

    with pytest.raises(AttributeError):
        _ = digital_waveform_from_protobuf(digital_waveform_proto)


def test___digital_waveform_proto_signal_count_zero___convert___raises_value_error() -> None:
    digital_waveform_proto = DigitalWaveformProto(y_data=b"", signal_count=0)

    with pytest.raises(ValueError) as exc:
        _ = digital_waveform_from_protobuf(digital_waveform_proto)

    assert exc.value.args[0].startswith("signal_count must be greater than zero.")


def _to_proto_timestamps(timestamps: list[dt.datetime]) -> list[PrecisionTimestamp]:
    return [bintime_datetime_to_protobuf(bt.DateTime(ts)) for ts in timestamps]


def _assert_proto_standard_timing(
    waveform_proto: (
        DoubleAnalogWaveform
        | DoubleComplexWaveform
        | I16AnalogWaveform
        | I16ComplexWaveform
        | DigitalWaveformProto
    ),
    t0_dt: dt.datetime,
) -> None:
    assert waveform_proto.dt == 1.0
    assert waveform_proto.t0 == bintime_datetime_to_protobuf(bt.DateTime(t0_dt))


def _assert_proto_standard_timing_with_offset(
    waveform_proto: (
        DoubleAnalogWaveform
        | DoubleComplexWaveform
        | I16AnalogWaveform
        | I16ComplexWaveform
        | DigitalWaveformProto
    ),
    t0_dt: dt.datetime,
    time_offset: dt.timedelta,
) -> None:
    assert waveform_proto.dt == 1.0
    assert waveform_proto.t0 == bintime_datetime_to_protobuf(bt.DateTime(t0_dt + time_offset))


def _assert_waveform_timestamp_and_t0_timing(
    waveform: AnalogWaveform[Any] | ComplexWaveform[Any] | DigitalWaveform[Any],
    t0_seconds: int,
    timestamp_seconds: int,
    sample_interval: float,
    time_offset: float,
) -> None:
    bt_timestamp = convert_datetime(bt.DateTime, waveform.timing.timestamp)
    bt_start_time = convert_datetime(bt.DateTime, waveform.timing.start_time)
    assert timestamp_seconds == bintime_datetime_to_protobuf(bt_timestamp).seconds
    assert not bintime_datetime_to_protobuf(bt_timestamp).fractional_seconds
    assert t0_seconds == bintime_datetime_to_protobuf(bt_start_time).seconds
    assert not bintime_datetime_to_protobuf(bt_start_time).fractional_seconds
    assert waveform.timing.sample_interval == dt.timedelta(seconds=sample_interval)
    assert waveform.timing.time_offset == bt.TimeDelta(time_offset)
    assert waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR
