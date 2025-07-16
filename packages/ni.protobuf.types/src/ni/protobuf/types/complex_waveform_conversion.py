"""Methods to convert to and from waveform protobuf messages."""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping

import hightime as ht
import nitypes.bintime as bt
import numpy as np
from nitypes.complex import convert_complex, ComplexInt32Base, ComplexInt32DType
from nitypes.time import convert_datetime
from nitypes.waveform import (
    AnalogWaveform,
    ComplexWaveform,
    ExtendedPropertyDictionary,
    ExtendedPropertyValue,
    NoneScaleMode,
    Timing,
)

from ni.protobuf.types.precision_timestamp_conversion import (
    bintime_datetime_to_protobuf,
    bintime_datetime_from_protobuf,
)
from ni.protobuf.types.waveform_pb2 import (
    DoubleAnalogWaveform,
    DoubleComplexWaveform,
    I16ComplexWaveform,
    WaveformAttributeValue,
)


def float64_complex_waveform_to_protobuf(
    value: ComplexWaveform[np.complex128], /
) -> DoubleComplexWaveform:
    """Convert the Python ComplexWaveform to a protobuf DoubleComplexWaveform."""
    if value.timing.has_start_time:
        bin_datetime = convert_datetime(bt.DateTime, value.timing.start_time)
        precision_timestamp = bintime_datetime_to_protobuf(bin_datetime)
    else:
        precision_timestamp = None

    if value.timing.has_sample_interval:
        time_interval = value.timing.sample_interval.total_seconds()
    else:
        time_interval = 0

    attributes = _extended_properties_to_attributes(value.extended_properties)

    interleaved_array = []
    for scaled_value in value.scaled_data:
        interleaved_array.append(np.real(scaled_value))
        interleaved_array.append(np.imag(scaled_value))

    return DoubleComplexWaveform(
        t0=precision_timestamp,
        dt=time_interval,
        y_data=interleaved_array,
        attributes=attributes,
    )


def float64_complex_waveform_from_protobuf(
    message: DoubleComplexWaveform, /
) -> ComplexWaveform[np.complex128]:
    """Convert the protobuf DoubleComplexWaveform to a Python ComplexWaveform."""
    # Declare timing to accept both bintime and dt.datetime to satisfy mypy.
    timing: Timing[bt.DateTime | dt.datetime]
    if not message.dt and not message.HasField("t0"):
        # If both dt and t0 are unset, use Timing.empty.
        timing = Timing.empty
    else:
        # Timestamp
        bin_datetime = bintime_datetime_from_protobuf(message.t0)

        # Sample Interval
        if not message.dt:
            timing = Timing.create_with_no_interval(timestamp=bin_datetime)
        else:
            sample_interval = ht.timedelta(seconds=message.dt)
            timing = Timing.create_with_regular_interval(
                sample_interval=sample_interval,
                timestamp=bin_datetime,
            )

    extended_properties = {}
    for key, value in message.attributes.items():
        attr_type = value.WhichOneof("attribute")
        extended_properties[key] = getattr(value, str(attr_type))

    real_data = message.y_data[0::2]
    imaginary_data = message.y_data[1::2]
    if len(real_data) != len(imaginary_data):
        raise ValueError("Interleaved data must have an even number of elements.")

    complex_values = []
    for i in range(0, len(real_data)):
        complex_values.append(np.complex128(real_data[i], imaginary_data[i]))

    data_array = np.array(complex_values, np.complex128)
    print(complex_values)
    return ComplexWaveform.from_array_1d(
        data_array,
        extended_properties=extended_properties,
        timing=timing,
        scale_mode=NoneScaleMode(),
    )

# ==================================================

def int16_complex_waveform_to_protobuf(
    value: ComplexWaveform[ComplexInt32Base], /
) -> I16ComplexWaveform:
    """Convert the Python ComplexWaveform to a protobuf DoubleComplexWaveform."""
    if value.timing.has_start_time:
        bin_datetime = convert_datetime(bt.DateTime, value.timing.start_time)
        precision_timestamp = bintime_datetime_to_protobuf(bin_datetime)
    else:
        precision_timestamp = None

    if value.timing.has_sample_interval:
        time_interval = value.timing.sample_interval.total_seconds()
    else:
        time_interval = 0

    attributes = _extended_properties_to_attributes(value.extended_properties)

    scaled_array = convert_complex(ComplexInt32DType, value.scaled_data)
    interleaved_array = scaled_array.view(np.int16)
    # for scaled_value in value.scaled_data:
    #     interleaved_array.append(np.real(scaled_value))
    #     interleaved_array.append(np.imag(scaled_value))

    return DoubleComplexWaveform(
        t0=precision_timestamp,
        dt=time_interval,
        y_data=interleaved_array,
        attributes=attributes,
    )


def int16_complex_waveform_from_protobuf(
    message: I16ComplexWaveform, /
) -> ComplexWaveform[ComplexInt32Base]:
    """Convert the protobuf DoubleComplexWaveform to a Python ComplexWaveform."""
    # Declare timing to accept both bintime and dt.datetime to satisfy mypy.
    timing: Timing[bt.DateTime | dt.datetime]
    if not message.dt and not message.HasField("t0"):
        # If both dt and t0 are unset, use Timing.empty.
        timing = Timing.empty
    else:
        # Timestamp
        bin_datetime = bintime_datetime_from_protobuf(message.t0)

        # Sample Interval
        if not message.dt:
            timing = Timing.create_with_no_interval(timestamp=bin_datetime)
        else:
            sample_interval = ht.timedelta(seconds=message.dt)
            timing = Timing.create_with_regular_interval(
                sample_interval=sample_interval,
                timestamp=bin_datetime,
            )

    extended_properties = {}
    for key, value in message.attributes.items():
        attr_type = value.WhichOneof("attribute")
        extended_properties[key] = getattr(value, str(attr_type))

    y_array = np.array(message.y_data, np.int16)
    data_array = y_array.view(ComplexInt32DType)
    return ComplexWaveform.from_array_1d(
        data_array,
        extended_properties=extended_properties,
        timing=timing,
        scale_mode=NoneScaleMode(),
    )


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
