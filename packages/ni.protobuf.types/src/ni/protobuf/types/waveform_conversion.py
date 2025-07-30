"""Methods to convert to and from waveform protobuf messages."""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from typing import Any

import hightime as ht
import nitypes.bintime as bt
import numpy as np
from nitypes.complex import ComplexInt32Base, ComplexInt32DType
from nitypes.time import convert_datetime
from nitypes.waveform import (
    AnalogWaveform,
    ComplexWaveform,
    DigitalWaveform,
    ExtendedPropertyDictionary,
    LinearScaleMode,
    NoneScaleMode,
    SampleIntervalMode,
    Spectrum,
    Timing,
)
from nitypes.waveform.typing import ExtendedPropertyValue

import ni.protobuf.types.precision_timestamp_conversion as ptc
from ni.protobuf.types.precision_timestamp_pb2 import PrecisionTimestamp
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


def float64_analog_waveform_to_protobuf(
    value: AnalogWaveform[np.float64], /
) -> DoubleAnalogWaveform:
    """Convert the Python AnalogWaveform to a protobuf DoubleAnalogWaveform."""
    _validate_timing(value)
    t0 = _t0_from_waveform(value)
    time_interval = _time_interval_from_waveform(value)
    attributes = _extended_properties_to_attributes(value.extended_properties)

    return DoubleAnalogWaveform(
        t0=t0,
        dt=time_interval,
        y_data=value.scaled_data,
        attributes=attributes,
    )


def float64_analog_waveform_from_protobuf(
    message: DoubleAnalogWaveform, /
) -> AnalogWaveform[np.float64]:
    """Convert the protobuf DoubleAnalogWaveform to a Python AnalogWaveform."""
    timing = _timing_from_waveform_message(message)
    extended_properties = _attributes_to_extended_properties(message.attributes)

    return AnalogWaveform.from_array_1d(
        message.y_data,
        dtype=np.float64,
        extended_properties=extended_properties,
        timing=timing,
        scale_mode=NoneScaleMode(),
    )


def float64_complex_waveform_to_protobuf(
    value: ComplexWaveform[np.complex128], /
) -> DoubleComplexWaveform:
    """Convert the Python ComplexWaveform to a protobuf DoubleComplexWaveform."""
    _validate_timing(value)
    t0 = _t0_from_waveform(value)
    time_interval = _time_interval_from_waveform(value)
    attributes = _extended_properties_to_attributes(value.extended_properties)

    interleaved_array = value.scaled_data.view(np.float64)

    return DoubleComplexWaveform(
        t0=t0,
        dt=time_interval,
        y_data=interleaved_array,
        attributes=attributes,
    )


def float64_complex_waveform_from_protobuf(
    message: DoubleComplexWaveform, /
) -> ComplexWaveform[np.complex128]:
    """Convert the protobuf DoubleComplexWaveform to a Python ComplexWaveform."""
    timing = _timing_from_waveform_message(message)
    extended_properties = _attributes_to_extended_properties(message.attributes)

    y_array = np.array(message.y_data, np.float64)
    data_array = y_array.view(np.complex128)

    return ComplexWaveform.from_array_1d(
        data_array,
        copy=False,
        extended_properties=extended_properties,
        timing=timing,
        scale_mode=NoneScaleMode(),
    )


def int16_complex_waveform_to_protobuf(
    value: ComplexWaveform[ComplexInt32Base], /
) -> I16ComplexWaveform:
    """Convert the Python ComplexWaveform to a protobuf DoubleComplexWaveform."""
    _validate_timing(value)
    t0 = _t0_from_waveform(value)
    time_interval = _time_interval_from_waveform(value)
    attributes = _extended_properties_to_attributes(value.extended_properties)
    scale = _scale_from_waveform(value)

    interleaved_array = value.raw_data.view(np.int16)

    return I16ComplexWaveform(
        t0=t0,
        dt=time_interval,
        y_data=interleaved_array,
        attributes=attributes,
        scale=scale,
    )


def int16_complex_waveform_from_protobuf(
    message: I16ComplexWaveform, /
) -> ComplexWaveform[ComplexInt32Base]:
    """Convert the protobuf DoubleComplexWaveform to a Python ComplexWaveform."""
    timing = _timing_from_waveform_message(message)
    extended_properties = _attributes_to_extended_properties(message.attributes)
    scale_mode = _scale_mode_from_waveform_message(message)

    y_array = np.array(message.y_data, np.int16)
    data_array = y_array.view(ComplexInt32DType)

    return ComplexWaveform.from_array_1d(
        data_array,
        copy=False,
        extended_properties=extended_properties,
        timing=timing,
        scale_mode=scale_mode,
    )


def float64_spectrum_to_protobuf(value: Spectrum[np.float64], /) -> DoubleSpectrum:
    """Convert the Python Spectrum to a protobuf DoubleSpectrum."""
    attributes = _extended_properties_to_attributes(value.extended_properties)
    return DoubleSpectrum(
        start_frequency=value.start_frequency,
        frequency_increment=value.frequency_increment,
        data=value.data,
        attributes=attributes,
    )


def float64_spectrum_from_protobuf(message: DoubleSpectrum, /) -> Spectrum[np.float64]:
    """Convert the protobuf DoubleSpectrum to a Python Spectrum."""
    extended_properties = _attributes_to_extended_properties(message.attributes)
    return Spectrum.from_array_1d(
        message.data,
        dtype=np.float64,
        start_frequency=message.start_frequency,
        frequency_increment=message.frequency_increment,
        extended_properties=extended_properties,
    )


def int16_analog_waveform_to_protobuf(value: AnalogWaveform[np.int16], /) -> I16AnalogWaveform:
    """Convert the Python AnalogWaveform to a protobuf I16AnalogWaveform."""
    _validate_timing(value)
    t0 = _t0_from_waveform(value)
    time_interval = _time_interval_from_waveform(value)
    attributes = _extended_properties_to_attributes(value.extended_properties)
    scale = _scale_from_waveform(value)

    return I16AnalogWaveform(
        t0=t0,
        dt=time_interval,
        y_data=value.raw_data,
        attributes=attributes,
        scale=scale,
    )


def int16_analog_waveform_from_protobuf(message: I16AnalogWaveform, /) -> AnalogWaveform[np.int16]:
    """Convert the protobuf I16AnalogWaveform to a Python AnalogWaveform."""
    timing = _timing_from_waveform_message(message)
    extended_properties = _attributes_to_extended_properties(message.attributes)
    scale_mode = _scale_mode_from_waveform_message(message)

    return AnalogWaveform.from_array_1d(
        message.y_data,
        dtype=np.int16,
        extended_properties=extended_properties,
        timing=timing,
        scale_mode=scale_mode,
    )


def digital_waveform_to_protobuf(value: DigitalWaveform[Any], /) -> DigitalWaveformProto:
    """Convert the Python DigitalWaveform to a protobuf DigitalWaveform."""
    _validate_timing(value)
    t0 = _t0_from_waveform(value)
    time_interval = _time_interval_from_waveform(value)
    attributes = _extended_properties_to_attributes(value.extended_properties)

    return DigitalWaveformProto(
        t0=t0,
        dt=time_interval,
        signal_count=value.signal_count,
        y_data=value.data.tobytes(),
        attributes=attributes,
    )


def digital_waveform_from_protobuf(message: DigitalWaveformProto, /) -> DigitalWaveform[np.uint8]:
    """Convert the protobuf DigitalWaveform to a Python DigitalWaveform."""
    timing = _timing_from_waveform_message(message)
    extended_properties = _attributes_to_extended_properties(message.attributes)

    if message.signal_count <= 0:
        raise ValueError("signal_count must be greater than zero.")

    data_array = np.frombuffer(message.y_data, dtype=np.uint8)
    samples_per_signal = len(data_array) // message.signal_count
    if len(data_array) != samples_per_signal * message.signal_count:
        raise ValueError(f"Data array length ({len(data_array)}) does not match expected shape.")
    reshaped_data = data_array.reshape(samples_per_signal, message.signal_count)

    return DigitalWaveform.from_lines(
        reshaped_data,
        dtype=np.uint8,
        signal_count=message.signal_count,
        extended_properties=extended_properties,
        timing=timing,
    )


def _attributes_to_extended_properties(
    attributes: Mapping[str, WaveformAttributeValue],
) -> Mapping[str, ExtendedPropertyValue]:
    extended_properties = {}
    for key, value in attributes.items():
        attr_type = value.WhichOneof("attribute")
        if attr_type is None:
            raise ValueError("Could not determine the datatype of 'attribute'.")
        extended_properties[key] = getattr(value, attr_type)

    return extended_properties


def _extended_properties_to_attributes(
    extended_properties: ExtendedPropertyDictionary,
) -> Mapping[str, WaveformAttributeValue]:
    return {key: _value_to_attribute(value) for key, value in extended_properties.items()}


def _value_to_attribute(value: ExtendedPropertyValue) -> WaveformAttributeValue:
    attr_value = WaveformAttributeValue()
    if isinstance(value, bool):
        attr_value.bool_value = value
    elif isinstance(value, int):
        attr_value.integer_value = value
    elif isinstance(value, float):
        attr_value.double_value = value
    elif isinstance(value, str):
        attr_value.string_value = value
    else:
        raise TypeError(f"Unexpected type for extended property value {type(value)}")

    return attr_value


def _validate_timing(
    waveform: AnalogWaveform[Any] | ComplexWaveform[Any] | DigitalWaveform[Any],
) -> None:
    if waveform.timing.sample_interval_mode == SampleIntervalMode.IRREGULAR:
        raise ValueError("Cannot convert irregular sample interval to protobuf.")


def _t0_from_waveform(
    waveform: AnalogWaveform[Any] | ComplexWaveform[Any] | DigitalWaveform[Any],
) -> PrecisionTimestamp | None:
    if waveform.timing.has_start_time:
        bin_datetime = convert_datetime(bt.DateTime, waveform.timing.start_time)
        return ptc.bintime_datetime_to_protobuf(bin_datetime)
    else:
        return None


def _time_interval_from_waveform(
    waveform: AnalogWaveform[Any] | ComplexWaveform[Any] | DigitalWaveform[Any],
) -> float:
    if waveform.timing.has_sample_interval:
        return waveform.timing.sample_interval.total_seconds()
    else:
        return 0


def _timing_from_waveform_message(
    message: (
        DoubleAnalogWaveform
        | DoubleComplexWaveform
        | I16AnalogWaveform
        | I16ComplexWaveform
        | DigitalWaveformProto
    ),
) -> Timing[bt.DateTime | dt.datetime]:
    # Declare timing to accept both bintime and dt.datetime to satisfy mypy.
    timing: Timing[bt.DateTime | dt.datetime]
    if not message.dt and not message.HasField("t0"):
        # If both dt and t0 are unset, use Timing.empty.
        timing = Timing.empty
    else:
        # Timestamp
        bin_datetime = ptc.bintime_datetime_from_protobuf(message.t0)

        # Sample Interval
        if not message.dt:
            timing = Timing.create_with_no_interval(timestamp=bin_datetime)
        else:
            sample_interval = ht.timedelta(seconds=message.dt)
            timing = Timing.create_with_regular_interval(
                sample_interval=sample_interval,
                timestamp=bin_datetime,
            )

    return timing


def _scale_from_waveform(waveform: AnalogWaveform[Any] | ComplexWaveform[Any]) -> Scale | None:
    if isinstance(waveform.scale_mode, LinearScaleMode):
        linear_scale = LinearScale(gain=waveform.scale_mode.gain, offset=waveform.scale_mode.offset)
        return Scale(linear_scale=linear_scale)
    elif isinstance(waveform.scale_mode, NoneScaleMode):
        return None
    else:
        raise ValueError(f"The waveform scale mode {waveform.scale_mode} is not supported.")


def _scale_mode_from_waveform_message(
    message: I16AnalogWaveform | I16ComplexWaveform,
) -> LinearScaleMode | NoneScaleMode:
    if message.HasField("scale"):
        mode = message.scale.WhichOneof("mode")
        if mode is None:
            raise ValueError("Could not determine waveform scale mode.")
        elif mode == "linear_scale":
            return LinearScaleMode(
                message.scale.linear_scale.gain, message.scale.linear_scale.offset
            )
        else:
            raise ValueError(f"The waveform scale mode {mode!r} is not supported.")

    return NoneScaleMode()
