import datetime as dt

import nitypes.bintime as bt
import numpy as np
import pytest
from nitypes.complex import ComplexInt32DType
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
    analog_waveform.unit_description = "Volts"

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

    assert dbl_analog_waveform.dt == 1.0
    bin_dt = bt.DateTime(t0_dt)
    converted_t0 = bintime_datetime_to_protobuf(bin_dt)
    assert dbl_analog_waveform.t0 == converted_t0


def test___analog_waveform_with_irregular_timing___convert___raises_value_error() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1.0, 2.0, 3.0]))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    analog_waveform.timing = Timing.create_with_irregular_interval(
        [t0_dt, t0_dt + dt.timedelta(milliseconds=1000), t0_dt + dt.timedelta(milliseconds=3000)]
    )

    with pytest.raises(ValueError) as exc:
        _ = float64_analog_waveform_to_protobuf(analog_waveform)

    assert exc.value.args[0].startswith("Cannot convert irregular sample interval to protobuf.")


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
    assert analog_waveform.unit_description == "Volts"


def test___dbl_analog_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleAnalogWaveform(t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0])

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_analog_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    dbl_analog_wfm = DoubleAnalogWaveform(dt=0.1, y_data=[1.0, 2.0, 3.0])

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
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
    complex_waveform.unit_description = "Volts"

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

    assert dbl_complex_waveform.dt == 1.0
    bin_dt = bt.DateTime(t0_dt)
    converted_t0 = bintime_datetime_to_protobuf(bin_dt)
    assert dbl_complex_waveform.t0 == converted_t0


def test___float64_complex_waveform_with_irregular_timing___convert___raises_value_error() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    complex_waveform.timing = Timing.create_with_irregular_interval(
        [t0_dt, t0_dt + dt.timedelta(milliseconds=1000)]
    )

    with pytest.raises(ValueError) as exc:
        _ = float64_complex_waveform_to_protobuf(complex_waveform)

    assert exc.value.args[0].startswith("Cannot convert irregular sample interval to protobuf.")


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
    assert complex_waveform.unit_description == "Volts"


def test___dbl_complex_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_complex_waveform = DoubleComplexWaveform(t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0])

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert complex_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert complex_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___dbl_complex_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    dbl_complex_waveform = DoubleComplexWaveform(dt=0.1, y_data=[1.0, 2.0, 3.0, 4.0])

    complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

    assert complex_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
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
    complex_waveform.unit_description = "Volts"

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

    assert i16_complex_waveform.dt == 1.0
    bin_dt = bt.DateTime(t0_dt)
    converted_t0 = bintime_datetime_to_protobuf(bin_dt)
    assert i16_complex_waveform.t0 == converted_t0


def test___int16_complex_waveform_with_irregular_timing___convert___raises_value_error() -> None:
    complex_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    complex_waveform.timing = Timing.create_with_irregular_interval(
        [t0_dt, t0_dt + dt.timedelta(milliseconds=1000)]
    )

    with pytest.raises(ValueError) as exc:
        _ = int16_complex_waveform_to_protobuf(complex_waveform)

    assert exc.value.args[0].startswith("Cannot convert irregular sample interval to protobuf.")


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
    print(i16_complex_waveform.HasField("scale"))

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
    assert complex_waveform.unit_description == "Volts"


def test___int16_complex_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_complex_waveform = I16ComplexWaveform(t0=t0_pt, dt=0.1, y_data=[1, 2, 3, 4])

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert complex_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert complex_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___int16_complex_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    i16_complex_waveform = I16ComplexWaveform(dt=0.1, y_data=[1, 2, 3, 4])

    complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

    assert complex_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
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
    analog_waveform.unit_description = "Volts"

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

    assert i16_analog_waveform.dt == 1.0
    bin_dt = bt.DateTime(t0_dt)
    converted_t0 = bintime_datetime_to_protobuf(bin_dt)
    assert i16_analog_waveform.t0 == converted_t0


def test___int16_analog_waveform_with_irregular_timing___convert___raises_value_error() -> None:
    analog_waveform = AnalogWaveform.from_array_1d(np.array([1, 2, 3], dtype=np.int16))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    analog_waveform.timing = Timing.create_with_irregular_interval(
        [t0_dt, t0_dt + dt.timedelta(milliseconds=1000), t0_dt + dt.timedelta(milliseconds=3000)]
    )

    with pytest.raises(ValueError) as exc:
        _ = int16_analog_waveform_to_protobuf(analog_waveform)

    assert exc.value.args[0].startswith("Cannot convert irregular sample interval to protobuf.")


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
    assert analog_waveform.unit_description == "Volts"


def test___i16_analog_wfm_with_timing___convert___valid_python_object() -> None:
    t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    i16_analog_wfm = I16AnalogWaveform(t0=t0_pt, dt=0.1, y_data=[1, 2, 3])

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert analog_waveform.timing.sample_interval == dt.timedelta(seconds=0.1)
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


def test___i16_analog_wfm_with_timing_no_t0___convert___valid_python_object() -> None:
    i16_analog_wfm = I16AnalogWaveform(dt=0.1, y_data=[1, 2, 3])

    analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

    assert analog_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
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
    spectrum.unit_description = "Volts"

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
    assert spectrum.unit_description == "Volts"


# ========================================================
# DigitalWaveform to DigitalWaveform
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
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    assert digital_waveform_proto.y_data == data.tobytes()
    assert digital_waveform_proto.signal_count == 3


def test___digital_waveform_with_extended_properties___convert___valid_protobuf() -> None:
    digital_waveform = DigitalWaveform()
    digital_waveform.channel_name = "Dev1/port0"

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    assert digital_waveform_proto.attributes["NI_ChannelName"].string_value == "Dev1/port0"


def test___digital_waveform_with_standard_timing___convert___valid_protobuf() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    digital_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

    assert digital_waveform_proto.dt == 1.0
    bin_dt = bt.DateTime(t0_dt)
    converted_t0 = bintime_datetime_to_protobuf(bin_dt)
    assert digital_waveform_proto.t0 == converted_t0
    assert digital_waveform_proto.signal_count == 3


def test___digital_waveform_with_irregular_timing___convert___raises_value_error() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    digital_waveform.timing = Timing.create_with_irregular_interval(
        [t0_dt, t0_dt + dt.timedelta(milliseconds=1000)]
    )

    with pytest.raises(ValueError) as exc:
        _ = digital_waveform_to_protobuf(digital_waveform)

    assert exc.value.args[0].startswith("Cannot convert irregular sample interval to protobuf.")


# ========================================================
# DigitalWaveform to DigitalWaveform
# ========================================================
def test___default_digital_waveform_proto___convert___valid_python_object() -> None:
    digital_waveform_proto = DigitalWaveformProto()

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert not digital_waveform.extended_properties
    assert digital_waveform.timing == Timing.empty
    assert digital_waveform.data.size == 0
    assert digital_waveform.signal_count == 0


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
    digital_waveform_proto = DigitalWaveformProto(attributes=attributes)

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


def test___digital_waveform_proto_with_timing_no_t0___convert___valid_python_object() -> None:
    data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
    digital_waveform_proto = DigitalWaveformProto(dt=0.1, y_data=data.tobytes(), signal_count=3)

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert digital_waveform.timing.start_time == dt.datetime(1904, 1, 1, tzinfo=dt.timezone.utc)
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


def test___digital_waveform_proto_empty_data___convert___valid_python_object() -> None:
    digital_waveform_proto = DigitalWaveformProto(y_data=b"", signal_count=0)

    digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

    assert digital_waveform.data.size == 0
    assert digital_waveform.signal_count == 0
