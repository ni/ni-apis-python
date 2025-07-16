import datetime as dt

import numpy
from nitypes.bintime import DateTime
from nitypes.waveform import (
    AnalogWaveform,
    NoneScaleMode,
    SampleIntervalMode,
    Spectrum,
    Timing,
)

from ni.protobuf.types.precision_timestamp_conversion import (
    bintime_datetime_to_protobuf,
)
from ni.protobuf.types.waveform_conversion import (
    float64_analog_waveform_from_protobuf,
    float64_analog_waveform_to_protobuf,
    float64_spectrum_waveform_from_protobuf,
    float64_spectrum_waveform_to_protobuf,
)
from ni.protobuf.types.waveform_pb2 import (
    DoubleAnalogWaveform,
    DoubleSpectrum,
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
    analog_waveform = AnalogWaveform.from_array_1d(numpy.array([1.0, 2.0, 3.0]))

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
    analog_waveform = AnalogWaveform.from_array_1d(numpy.array([1.0, 2.0, 3.0]))
    t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
    analog_waveform.timing = Timing.create_with_regular_interval(
        sample_interval=dt.timedelta(milliseconds=1000),
        timestamp=t0_dt,
    )

    dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

    assert dbl_analog_waveform.dt == 1.0
    bin_dt = DateTime(t0_dt)
    converted_t0 = bintime_datetime_to_protobuf(bin_dt)
    assert dbl_analog_waveform.t0 == converted_t0


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
    t0_dt = DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
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
    t0_dt = DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
    t0_pt = bintime_datetime_to_protobuf(t0_dt)
    dbl_analog_wfm = DoubleAnalogWaveform(t0=t0_pt, y_data=[1.0, 2.0, 3.0])

    analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

    assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
    assert not analog_waveform.timing.has_sample_interval
    assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE


# ========================================================
# Spectrum to DoubleSpectrum
# ========================================================
def test___default_spectrum___convert___valid_protobuf() -> None:
    spectrum_waveform = Spectrum()

    dbl_spectrum_waveform = float64_spectrum_waveform_to_protobuf(spectrum_waveform)

    assert not dbl_spectrum_waveform.attributes
    assert spectrum_waveform.start_frequency == 0.0
    assert spectrum_waveform.frequency_increment == 0.0
    assert list(dbl_spectrum_waveform.data) == []


def test___spectrum_with_data___convert___valid_protobuf() -> None:
    spectrum_waveform = Spectrum.from_array_1d(numpy.array([1.0, 2.0, 3.0]))
    spectrum_waveform.start_frequency = 100.0
    spectrum_waveform.frequency_increment = 10.0

    dbl_spectrum_waveform = float64_spectrum_waveform_to_protobuf(spectrum_waveform)

    assert list(dbl_spectrum_waveform.data) == [1.0, 2.0, 3.0]
    assert dbl_spectrum_waveform.start_frequency == 100.0
    assert dbl_spectrum_waveform.frequency_increment == 10.0


def test___spectrum_with_extended_properties___convert___valid_protobuf() -> None:
    spectrum_waveform = Spectrum()
    spectrum_waveform.channel_name = "Dev1/ai0"
    spectrum_waveform.unit_description = "Volts"

    dbl_spectrum_waveform = float64_spectrum_waveform_to_protobuf(spectrum_waveform)

    assert dbl_spectrum_waveform.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert dbl_spectrum_waveform.attributes["NI_UnitDescription"].string_value == "Volts"


# ========================================================
# DoubleSpectrum to Spectrum
# ========================================================
def test___default_dbl_spectrum___convert___valid_python_object() -> None:
    dbl_spectrum = DoubleSpectrum()

    spectrum_waveform = float64_spectrum_waveform_from_protobuf(dbl_spectrum)

    assert not spectrum_waveform.extended_properties
    assert spectrum_waveform.start_frequency == 0.0
    assert spectrum_waveform.frequency_increment == 0.0
    assert spectrum_waveform.sample_count == 0
    assert spectrum_waveform.data.size == 0


def test___dbl_spectrum_with_data___convert___valid_python_object() -> None:
    dbl_spectrum = DoubleSpectrum(
        data=[1.0, 2.0, 3.0], start_frequency=100.0, frequency_increment=10.0
    )

    spectrum_waveform = float64_spectrum_waveform_from_protobuf(dbl_spectrum)

    assert list(spectrum_waveform.data) == [1.0, 2.0, 3.0]
    assert spectrum_waveform.start_frequency == 100.0
    assert spectrum_waveform.frequency_increment == 10.0


def test___dbl_spectrum_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    dbl_spectrum = DoubleSpectrum(attributes=attributes)

    spectrum_waveform = float64_spectrum_waveform_from_protobuf(dbl_spectrum)

    assert spectrum_waveform.channel_name == "Dev1/ai0"
    assert spectrum_waveform.unit_description == "Volts"
