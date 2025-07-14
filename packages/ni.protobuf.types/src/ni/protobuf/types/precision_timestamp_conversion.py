"""Methods to convert to and from PrecisionTimestamp protobuf messages."""

from __future__ import annotations

import nitypes.bintime as bt

from ni.protobuf.types.precision_timestamp_pb2 import (
    PrecisionTimestamp,
)


def bintime_datetime_to_protobuf(value: bt.DateTime, /) -> PrecisionTimestamp:
    """Convert the NI-BTF DateTime to a protobuf PrecisionTimestamp."""
    seconds, fractional_seconds = value.to_tuple()
    return PrecisionTimestamp(seconds=seconds, fractional_seconds=fractional_seconds)


def bintime_datetime_from_protobuf(message: PrecisionTimestamp, /) -> bt.DateTime:
    """Convert the protobuf PrecisionTimestamp to a NI-BTF DateTime."""
    time_value_tuple = bt.TimeValueTuple(message.seconds, message.fractional_seconds)
    return bt.DateTime.from_tuple(time_value_tuple)
