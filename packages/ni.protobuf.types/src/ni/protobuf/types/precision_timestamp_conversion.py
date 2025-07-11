"""Methods to convert to and from PrecisionTimestamp protobuf messages."""

from __future__ import annotations

import nitypes.bintime as bt

from ni.protobuf.types.precision_timestamp_pb2 import (
    PrecisionTimestamp,
)


def bintime_datetime_to_protobuf(value: bt.DateTime, /) -> PrecisionTimestamp:
    """Convert the Python DateTime to a protobuf PrecisionTimestamp."""
    seconds, fractional_seconds = value.to_tuple()
    return PrecisionTimestamp(seconds=seconds, fractional_seconds=fractional_seconds)


def precision_timestamp_to_python(protobuf_message: PrecisionTimestamp) -> bt.DateTime:
    """Convert the protobuf PrecisionTimestamp to a Python DateTime."""
    time_value_tuple = bt.TimeValueTuple(
        protobuf_message.seconds, protobuf_message.fractional_seconds
    )
    return bt.DateTime.from_tuple(time_value_tuple)
