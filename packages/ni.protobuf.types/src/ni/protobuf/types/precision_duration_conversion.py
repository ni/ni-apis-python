"""Methods to convert to and from PrecisionDuration protobuf messages."""

from __future__ import annotations

import hightime as ht
import nitypes.bintime as bt
from nitypes.time import convert_timedelta

from ni.protobuf.types.precision_duration_pb2 import (
    PrecisionDuration,
)


def bintime_timedelta_to_protobuf(value: bt.TimeDelta, /) -> PrecisionDuration:
    """Convert a NI-BTF TimeDelta to a protobuf PrecisionDuration."""
    seconds, fractional_seconds = value.to_tuple()
    return PrecisionDuration(seconds=seconds, fractional_seconds=fractional_seconds)


def bintime_timedelta_from_protobuf(message: PrecisionDuration, /) -> bt.TimeDelta:
    """Convert a protobuf PrecisionDuration to a NI-BTF TimeDelta."""
    time_value_tuple = bt.TimeValueTuple(message.seconds, message.fractional_seconds)
    return bt.TimeDelta.from_tuple(time_value_tuple)


def hightime_timedelta_to_protobuf(value: ht.timedelta, /) -> PrecisionDuration:
    """Convert a hightime.timedelta to a protobuf PrecisionDuration."""
    bt_timedelta = convert_timedelta(bt.TimeDelta, value)
    return bintime_timedelta_to_protobuf(bt_timedelta)


def hightime_timedelta_from_protobuf(message: PrecisionDuration, /) -> ht.timedelta:
    """Convert a protobuf PrecisionDuration to a hightime.timedelta."""
    bt_timedelta = bintime_timedelta_from_protobuf(message)
    ht_timedelta = convert_timedelta(ht.timedelta, bt_timedelta)
    return ht_timedelta
