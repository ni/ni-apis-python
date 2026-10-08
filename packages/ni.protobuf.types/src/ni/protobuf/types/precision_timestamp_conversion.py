"""Methods to convert to and from PrecisionTimestamp protobuf messages."""

from __future__ import annotations

import datetime as dt

import hightime as ht
import nitypes.bintime as bt
from nitypes.time import convert_datetime

from ni.protobuf.types.precision_timestamp_pb2 import (
    PrecisionTimestamp,
)


def _hightime_datetime_to_utc(value: ht.datetime, /) -> ht.datetime:
    """Convert a hightime.datetime to UTC while preserving date-specific offsets."""
    if value.tzinfo is None:
        raise ValueError("value must be timezone-aware")
    offset = value.utcoffset() or dt.timedelta()
    return (value - offset).replace(tzinfo=dt.timezone.utc)


def bintime_datetime_to_protobuf(value: bt.DateTime, /) -> PrecisionTimestamp:
    """Convert a NI-BTF DateTime to a protobuf PrecisionTimestamp."""
    seconds, fractional_seconds = value.to_tuple()
    return PrecisionTimestamp(seconds=seconds, fractional_seconds=fractional_seconds)


def bintime_datetime_from_protobuf(message: PrecisionTimestamp, /) -> bt.DateTime:
    """Convert a protobuf PrecisionTimestamp to a NI-BTF DateTime."""
    time_value_tuple = bt.TimeValueTuple(message.seconds, message.fractional_seconds)
    return bt.DateTime.from_tuple(time_value_tuple)


def hightime_datetime_to_protobuf(value: ht.datetime, /) -> PrecisionTimestamp:
    """Convert a hightime.datetime to a protobuf PrecisionTimestamp.

    The hightime.datetime input will be converted to UTC as part of
    the protobuf conversion.
    """
    value_utc = _hightime_datetime_to_utc(value)
    bt_datetime = convert_datetime(bt.DateTime, value_utc)
    return bintime_datetime_to_protobuf(bt_datetime)


def hightime_datetime_from_protobuf(message: PrecisionTimestamp, /) -> ht.datetime:
    """Convert a protobuf PrecisionTimestamp to a hightime.datetime."""
    bt_datetime = bintime_datetime_from_protobuf(message)
    ht_datetime = convert_datetime(ht.datetime, bt_datetime)
    return ht_datetime
