import datetime as dt
from zoneinfo import ZoneInfo

import hightime as ht
import nitypes.bintime as bt
import pytest
from nitypes.time import convert_datetime
from tzlocal import get_localzone

from ni.protobuf.types.precision_timestamp_conversion import (
    _hightime_datetime_to_utc,
    bintime_datetime_from_protobuf,
    bintime_datetime_to_protobuf,
    hightime_datetime_from_protobuf,
    hightime_datetime_to_protobuf,
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
    ht_datetime = ht.datetime(
        year=2020,
        month=1,
        day=1,
        hour=5,
        minute=26,
        tzinfo=dt.timezone(dt.timedelta(hours=-7)),
    )

    pts = hightime_datetime_to_protobuf(ht_datetime)

    ht_datetime_utc = ht_datetime.astimezone(dt.timezone.utc)
    bt_datetime = convert_datetime(bt.DateTime, ht_datetime_utc)
    time_value = bt_datetime.to_tuple()
    assert pts.seconds == time_value.whole_seconds
    assert pts.fractional_seconds == time_value.fractional_seconds


# ========================================================
# _hightime_datetime_to_utc
# ========================================================
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            # Pre 1904
            ht.datetime(
                year=1900,
                month=1,
                day=1,
                hour=5,
                minute=26,
                tzinfo=dt.timezone(dt.timedelta(hours=5)),
            ),
            ht.datetime(year=1900, month=1, day=1, hour=0, minute=26, tzinfo=dt.timezone.utc),
        ),
        (
            # NI-BTF Epoch
            ht.datetime(year=1904, month=1, day=1, tzinfo=dt.timezone.utc),
            ht.datetime(year=1904, month=1, day=1, tzinfo=dt.timezone.utc),
        ),
        (
            # Between 1904 and 1970
            ht.datetime(
                year=1960,
                month=1,
                day=1,
                hour=5,
                minute=26,
                tzinfo=dt.timezone(dt.timedelta(hours=5)),
            ),
            ht.datetime(year=1960, month=1, day=1, hour=0, minute=26, tzinfo=dt.timezone.utc),
        ),
        (
            # After 1970
            ht.datetime(
                year=2020,
                month=6,
                day=1,
                hour=12,
                minute=30,
                tzinfo=dt.timezone(dt.timedelta(hours=-5, minutes=-30)),
            ),
            ht.datetime(
                year=2020,
                month=6,
                day=1,
                hour=18,
                tzinfo=dt.timezone.utc,
            ),
        ),
        (
            # Timezone already UTC
            ht.datetime(year=2020, month=1, day=1, hour=5, minute=26, tzinfo=dt.timezone.utc),
            ht.datetime(year=2020, month=1, day=1, hour=5, minute=26, tzinfo=dt.timezone.utc),
        ),
    ],
)
def test___hightime_datetime___to_utc___correct_utc_datetime(
    value: ht.datetime, expected: ht.datetime
) -> None:
    assert _hightime_datetime_to_utc(value) == expected


def test___hightime_datetime_local_timezone___to_utc___correct_utc_datetime() -> None:
    local_timezone = get_localzone()
    value = ht.datetime(year=2020, month=1, day=1, hour=12, tzinfo=local_timezone)
    expected = dt.datetime(2020, 1, 1, 12, tzinfo=local_timezone).astimezone(dt.timezone.utc)

    assert _hightime_datetime_to_utc(value) == ht.datetime(
        year=expected.year,
        month=expected.month,
        day=expected.day,
        hour=expected.hour,
        minute=expected.minute,
        second=expected.second,
        microsecond=expected.microsecond,
        tzinfo=expected.tzinfo,
    )


def test___hightime_datetime_zoneinfo_timezone_with_dst___to_utc___correct_utc_datetime() -> None:
    daylight_saving_time = ZoneInfo("America/Chicago")
    summer_datetime = ht.datetime(year=2020, month=7, day=1, hour=12, tzinfo=daylight_saving_time)
    winter_datetime = ht.datetime(year=2020, month=1, day=1, hour=12, tzinfo=daylight_saving_time)

    assert _hightime_datetime_to_utc(summer_datetime) == ht.datetime(
        year=2020,
        month=7,
        day=1,
        hour=17,
        tzinfo=dt.timezone.utc,
    )
    assert _hightime_datetime_to_utc(winter_datetime) == ht.datetime(
        year=2020,
        month=1,
        day=1,
        hour=18,
        tzinfo=dt.timezone.utc,
    )


def test___hightime_datetime_timezone_naive___to_utc___raises() -> None:
    with pytest.raises(ValueError, match="value must be timezone-aware"):
        _hightime_datetime_to_utc(ht.datetime(year=2020, month=1, day=1))


def test___hightime_datetime_timezone_without_offset___to_utc___raises() -> None:
    class NaiveTimezone(dt.tzinfo):
        def utcoffset(self, value: dt.datetime | None) -> dt.timedelta | None:
            return None

        def dst(self, value: dt.datetime | None) -> dt.timedelta | None:
            return None

        def tzname(self, value: dt.datetime | None) -> str | None:
            return "NaiveTimezone"

    value = ht.datetime(year=2020, month=1, day=1, tzinfo=NaiveTimezone())

    with pytest.raises(ValueError, match="value must be timezone-aware"):
        _hightime_datetime_to_utc(value)
