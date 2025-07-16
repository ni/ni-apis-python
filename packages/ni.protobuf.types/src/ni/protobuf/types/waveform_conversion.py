"""Methods to convert to and from waveform protobuf messages."""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping

import hightime as ht
import nitypes.bintime as bt
import numpy as np
from nitypes.time import convert_datetime
from nitypes.waveform import (
    AnalogWaveform,
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
    WaveformAttributeValue,
)


def float64_analog_waveform_to_protobuf(
    value: AnalogWaveform[np.float64], /
) -> DoubleAnalogWaveform:
    """Convert the Python AnalogWaveform to a protobuf DoubleAnalogWaveform."""
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

    return DoubleAnalogWaveform(
        t0=precision_timestamp,
        dt=time_interval,
        y_data=value.scaled_data,
        attributes=attributes,
    )


def float64_analog_waveform_from_protobuf(
    message: DoubleAnalogWaveform, /
) -> AnalogWaveform[np.float64]:
    """Convert the protobuf DoubleAnalogWaveform to a Python AnalogWaveform."""
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
        if attr_type is None:
            raise ValueError("Could not determine the datatype of 'attribute'.")
        extended_properties[key] = getattr(value, attr_type)

    data_array = np.array(message.y_data)
    return AnalogWaveform(
        sample_count=data_array.size,
        dtype=np.float64,
        raw_data=data_array,
        start_index=0,
        capacity=data_array.size,
        extended_properties=extended_properties,
        copy_extended_properties=True,
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
