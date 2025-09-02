import hightime as ht
import nitypes.bintime as bt
from nitypes.time import convert_timedelta

from ni.protobuf.types.precision_duration_conversion import (
    bintime_timedelta_to_protobuf,
    bintime_timedelta_from_protobuf,
    hightime_timedelta_to_protobuf,
    hightime_timedelta_from_protobuf,
)
from ni.protobuf.types.precision_duration_pb2 import PrecisionDuration


# ========================================================
# bintime.TimeDelta <--> PrecisionDuration
# ========================================================
def test___precision_duration___convert___valid_bintime_timedelta() -> None:
    seconds = 25
    fractional_seconds = 123
    pts = PrecisionDuration(seconds=seconds, fractional_seconds=fractional_seconds)

    bintime_timedelta = bintime_timedelta_from_protobuf(pts)

    time_value = bintime_timedelta.to_tuple()
    assert time_value.whole_seconds == seconds
    assert time_value.fractional_seconds == fractional_seconds


def test___bintime_timedelta___convert___valid_precision_duration() -> None:
    seconds = 25
    fractional_seconds = 123
    bintime_timedelta = bt.TimeDelta.from_tuple(bt.TimeValueTuple(seconds, fractional_seconds))

    pts = bintime_timedelta_to_protobuf(bintime_timedelta)

    assert pts.seconds == seconds
    assert pts.fractional_seconds == fractional_seconds


# ========================================================
# hightime.timedelta <--> PrecisionDuration
# ========================================================
def test___precision_duration___convert___valid_hightime_timedelta() -> None:
    seconds = 25
    fractional_seconds = 123
    pts = PrecisionDuration(seconds=seconds, fractional_seconds=fractional_seconds)

    ht_timedelta = hightime_timedelta_from_protobuf(pts)

    bt_timedelta = convert_timedelta(bt.TimeDelta, ht_timedelta)
    time_value = bt_timedelta.to_tuple()
    assert time_value.whole_seconds == seconds
    assert time_value.fractional_seconds == fractional_seconds


def test___hightime_timedelta___convert___valid_precision_duration() -> None:
    ht_timedelta = ht.timedelta(days=1, hours=5, minutes=26, seconds=35, picoseconds=7)

    pts = hightime_timedelta_to_protobuf(ht_timedelta)

    bt_timedelta = convert_timedelta(bt.TimeDelta, ht_timedelta)
    time_value = bt_timedelta.to_tuple()
    assert pts.seconds == time_value.whole_seconds
    assert pts.fractional_seconds == time_value.fractional_seconds
