import datetime as dt

import hightime as ht
import nitypes.bintime as bt
from nitypes.time import convert_datetime

from ni.protobuf.types.precision_timestamp_conversion import (
    bintime_datetime_to_protobuf,
    bintime_datetime_from_protobuf,
    hightime_datetime_to_protobuf,
    hightime_datetime_from_protobuf,
)
from ni.protobuf.types.precision_timestamp_pb2 import PrecisionTimestamp


# ========================================================
# bintime.DateTime <--> PrecisionTimestamp
# ========================================================
def test___precision_timestamp___convert___valid_bintime_datetime() -> None:
    seconds = 25
    fractional_seconds = 123
    pts = PrecisionTimestamp(seconds=seconds, fractional_seconds=fractional_seconds)

    bintime_datetime = bintime_datetime_from_protobuf(pts)

    time_value = bintime_datetime.to_tuple()
    assert time_value.whole_seconds == seconds
    assert time_value.fractional_seconds == fractional_seconds


def test___bintime_datetime___convert___valid_precision_timestamp() -> None:
    seconds = 25
    fractional_seconds = 123
    bintime_datetime = bt.DateTime.from_tuple(bt.TimeValueTuple(seconds, fractional_seconds))

    pts = bintime_datetime_to_protobuf(bintime_datetime)

    assert pts.seconds == seconds
    assert pts.fractional_seconds == fractional_seconds


# ========================================================
# hightime.datetime <--> PrecisionTimestamp
# ========================================================
def test___precision_timestamp___convert___valid_hightime_datetime() -> None:
    seconds = 25
    fractional_seconds = 123
    pts = PrecisionTimestamp(seconds=seconds, fractional_seconds=fractional_seconds)

    ht_datetime = hightime_datetime_from_protobuf(pts)

    bt_datetime = convert_datetime(bt.DateTime, ht_datetime)
    time_value = bt_datetime.to_tuple()
    assert time_value.whole_seconds == seconds
    assert time_value.fractional_seconds == fractional_seconds


def test___hightime_datetime___convert___valid_precision_timestamp() -> None:
    ht_datetime = ht.datetime(year=2020, month=1, day=1, hour=5, minute=26, tzinfo=dt.timezone.utc)

    pts = hightime_datetime_to_protobuf(ht_datetime)

    bt_datetime = convert_datetime(bt.DateTime, ht_datetime)
    time_value = bt_datetime.to_tuple()
    assert pts.seconds == time_value.whole_seconds
    assert pts.fractional_seconds == time_value.fractional_seconds
