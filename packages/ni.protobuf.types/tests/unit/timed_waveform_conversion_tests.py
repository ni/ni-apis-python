"""Unit tests for conversion of the timing aspects of various types of waveforms."""

import datetime as dt
from abc import abstractmethod

import hightime as ht
import nitypes.bintime as bt
import pytest
from nitypes.time import convert_datetime
from nitypes.waveform import (
    NoneScaleMode,
    SampleIntervalMode,
    Timing,
)

from ni.protobuf.types.precision_timestamp_conversion import (
    bintime_datetime_to_protobuf,
)
from ni.protobuf.types.precision_timestamp_pb2 import PrecisionTimestamp
from ni.protobuf.types.waveform_conversion import (
    AnyNiWaveform,
    AnyWaveformProto,
)


# ========================================================
# Base class
# ========================================================
class TimedWaveformConversionTests:
    """Base class for testing waveform conversion.

    Subclasses implement more specific or typed waveform conversion tests.
    """

    @abstractmethod
    def make_waveform(self) -> AnyNiWaveform:
        """Create a waveform with small non-zero sample data."""
        ...

    @abstractmethod
    def make_waveform_proto(self) -> AnyWaveformProto:
        """Create a waveform protobuf object with small non-zero sample data."""
        ...

    @abstractmethod
    def to_protobuf(self, waveform: AnyNiWaveform) -> AnyWaveformProto:
        """Convert a Python waveform to its corresponding proto message."""
        ...

    @abstractmethod
    def from_protobuf(self, waveform_proto: AnyWaveformProto) -> AnyNiWaveform:
        """Convert a proto message to the corresponding Python waveform."""
        ...

    # ========================================================
    # To Protobuf
    # ========================================================
    def test___waveform_with_standard_timing___convert___valid_protobuf(self) -> None:
        """Test conversion of a waveform with standard timing."""
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        sample_interval_seconds = 1.5
        waveform.timing = Timing.create_with_regular_interval(
            sample_interval=dt.timedelta(seconds=sample_interval_seconds),
            timestamp=t0_dt,
        )

        waveform_proto = self.to_protobuf(waveform)

        self._assert_proto_standard_timing(waveform_proto, t0_dt, sample_interval_seconds)

    def test___waveform_with_standard_timing_and_offset___convert___valid_protobuf(self) -> None:
        """Test conversion of a waveform with standard timing and offset."""
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        sample_interval_seconds = 2.5
        sample_interval = dt.timedelta(seconds=sample_interval_seconds)
        time_offset = dt.timedelta(seconds=0.5)
        waveform.timing = Timing.create_with_regular_interval(
            sample_interval=sample_interval,
            timestamp=t0_dt,
            time_offset=time_offset,
        )

        waveform_proto = self.to_protobuf(waveform)

        self._assert_proto_standard_timing_with_offset(
            waveform_proto, t0_dt, time_offset, sample_interval_seconds
        )

    def test___waveform_with_standard_timing___round_trip___waveforms_match(self) -> None:
        """Test a round-trip conversion of a waveform with standard timing."""
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        sample_interval = dt.timedelta(seconds=1.5)
        time_offset = dt.timedelta(seconds=2.3)
        waveform.timing = Timing.create_with_regular_interval(
            sample_interval=sample_interval,
            timestamp=t0_dt,
            time_offset=time_offset,
        )

        waveform_proto = self.to_protobuf(waveform)
        converted_waveform = self.from_protobuf(waveform_proto)

        assert waveform == converted_waveform

    def test___waveform_with_irregular_timing___convert___valid_protobuf(self) -> None:
        """Test a conversion of a waveform with irregular timing."""
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        timestamps = [
            t0_dt,
            t0_dt + dt.timedelta(seconds=1.5),
        ]
        waveform.timing = Timing.create_with_irregular_interval(timestamps)

        waveform_proto = self.to_protobuf(waveform)

        assert list(waveform_proto.timestamps) == self._to_proto_timestamps(timestamps)

    @pytest.mark.parametrize(
        "timestamp_seconds, time_offset",
        [
            (0, 0),
            (0, 10.5),
            (100.5, 10.5),
            (100.5, 0),
        ],
    )
    def test___waveform_with_regular_timing___round_trip___waveforms_match(
        self, timestamp_seconds: int, time_offset: float
    ) -> None:
        """Test a round trip conversion of a waveform with regular timing."""
        sample_interval = 1  # Regular interval of 1s
        if timestamp_seconds:
            timestamp = convert_datetime(
                bt.DateTime, dt.datetime.fromtimestamp(timestamp_seconds, tz=dt.timezone.utc)
            )
        else:
            timestamp = None
        waveform = self.make_waveform()
        waveform.timing = Timing.create_with_regular_interval(
            sample_interval=ht.timedelta(seconds=sample_interval),
            timestamp=timestamp,
            time_offset=ht.timedelta(seconds=time_offset),
        )
        try:
            waveform.scale_mode = NoneScaleMode()  # type: ignore
        except AttributeError:
            pass  # Some waveforms don't support scaling

        waveform_proto = self.to_protobuf(waveform)
        converted_waveform = self.from_protobuf(waveform_proto)

        assert waveform == converted_waveform

    @pytest.mark.parametrize(
        "timestamp_seconds, time_offset",
        [
            (0, 0),
            (0, 10.5),
            (100.5, 10.5),
            (100.5, 0),
        ],
    )
    def test___waveform_with_none_timing___round_trip___waveforms_match(
        self, timestamp_seconds: int, time_offset: float
    ) -> None:
        """Test a round trip conversion of a waveform with None timing."""
        if timestamp_seconds:
            timestamp = convert_datetime(
                bt.DateTime, dt.datetime.fromtimestamp(timestamp_seconds, tz=dt.timezone.utc)
            )
        else:
            timestamp = None
        waveform = self.make_waveform()
        waveform.timing = Timing.create_with_no_interval(
            timestamp=timestamp,
            time_offset=ht.timedelta(seconds=time_offset),
        )
        try:
            waveform.scale_mode = NoneScaleMode()  # type: ignore
        except AttributeError:
            pass  # Some waveforms don't support scaling.

        waveform_proto = self.to_protobuf(waveform)
        converted_waveform = self.from_protobuf(waveform_proto)

        assert waveform == converted_waveform

    # ========================================================
    # From Protobuf
    # ========================================================
    def test___waveform_proto_with_timing___convert___valid_python_object(self) -> None:
        """Test conversion of a waveform proto with timing information."""
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0.CopyFrom(t0_pt)
        sample_interval_seconds = 0.1
        waveform_proto.dt = sample_interval_seconds

        waveform = self.from_protobuf(waveform_proto)

        assert waveform.timing.start_time == t0_dt._to_datetime_datetime()
        assert waveform.timing.sample_interval == ht.timedelta(seconds=sample_interval_seconds)
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR

    def test___waveform_proto_with_timing___round_trip___waveforms_match(self) -> None:
        """Test a round-trip conversion of a waveform proto with timing information."""
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0.CopyFrom(t0_pt)
        waveform_proto.dt = 0.1
        waveform_proto.timestamp.CopyFrom(t0_pt)
        waveform_proto.time_offset = 0.0

        waveform = self.from_protobuf(waveform_proto)
        converted_waveform_proto = self.to_protobuf(waveform)

        assert waveform_proto == converted_waveform_proto

    @pytest.mark.parametrize(
        "timestamp_seconds, start_time_seconds, offset, normalized_timestamp_seconds, normalized_start_time_seconds",
        [
            (0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (0, 10, 0, 10, 10),
            (100, 0, 0, 100, 100),
            (100, 0, 1, 100, 101),
            (100, 10, 0, 100, 100),
            (100, 10, 1, 100, 101),
        ],
    )
    def test___waveform_proto_regular_timing___round_trip___timing_equivalent(
        self,
        timestamp_seconds: int,
        start_time_seconds: int,
        offset: float,
        normalized_timestamp_seconds: int,
        normalized_start_time_seconds: int,
    ) -> None:
        """Test various round-trip conversions of a waveform proto with regular timing."""
        t0_pt = PrecisionTimestamp(seconds=start_time_seconds, fractional_seconds=0)
        timestamp_pt = PrecisionTimestamp(seconds=timestamp_seconds, fractional_seconds=0)
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0.CopyFrom(t0_pt)
        waveform_proto.dt = 0.1
        waveform_proto.timestamp.CopyFrom(timestamp_pt)
        waveform_proto.time_offset = offset

        waveform = self.from_protobuf(waveform_proto)
        converted_waveform_proto = self.to_protobuf(waveform)

        assert (
            normalized_timestamp_seconds
            == self._normalize_precision_timestamp(converted_waveform_proto.timestamp).seconds
        )
        assert (
            normalized_start_time_seconds
            == self._normalize_precision_timestamp(converted_waveform_proto.t0).seconds
        )

    def test___waveform_proto_with_timing_no_t0___convert___valid_python_object(self) -> None:
        """Test conversion of a waveform proto without t0."""
        waveform_proto = self.make_waveform_proto()
        waveform_proto.dt = 0.1

        waveform = self.from_protobuf(waveform_proto)

        assert not waveform.timing.has_start_time
        assert waveform.timing.sample_interval == ht.timedelta(seconds=0.1)
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR

    def test___waveform_proto_with_timing_no_dt___convert___valid_python_object(self) -> None:
        "Test conversion of a waveform proto without a dt."
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0.CopyFrom(t0_pt)

        waveform = self.from_protobuf(waveform_proto)

        assert waveform.timing.start_time == t0_dt._to_datetime_datetime()
        assert not waveform.timing.has_sample_interval
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.NONE

    def test___waveform_proto_with_dt_and_offset___convert___valid_python_object(self) -> None:
        """Test conversion of a waveform proto with dt and offset."""
        waveform_proto = self.make_waveform_proto()
        waveform_proto.dt = 0.1
        waveform_proto.time_offset = 1.5

        waveform = self.from_protobuf(waveform_proto)

        assert not waveform.timing.has_timestamp
        assert waveform.timing.sample_interval == ht.timedelta(seconds=0.1)
        assert waveform.timing.time_offset == ht.timedelta(seconds=1.5)
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR

    def test___waveform_proto_with_t0_and_timestamp_and_offset___convert___valid_python_object(
        self,
    ) -> None:
        """Test conversion of a waveform proto with t0, timestamp, and offset."""
        sample_interval = 0.1
        t0_seconds = 1000001
        t0_pt = PrecisionTimestamp(seconds=t0_seconds, fractional_seconds=0)
        timestamp_seconds = 1000000
        timestamp_pt = PrecisionTimestamp(seconds=timestamp_seconds, fractional_seconds=0)
        time_offset = 1.0
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0.CopyFrom(t0_pt)
        waveform_proto.dt = 0.1
        waveform_proto.timestamp.CopyFrom(timestamp_pt)
        waveform_proto.time_offset = time_offset

        waveform = self.from_protobuf(waveform_proto)

        self._assert_waveform_timestamp_and_t0_timing(
            waveform, t0_seconds, timestamp_seconds, sample_interval, time_offset
        )

    def test___waveform_proto_with_timestamps___convert___valid_python_object(self) -> None:
        """Test conversion of a waveform proto with timestamps (irregular timing)."""
        expected_timestamps = [
            PrecisionTimestamp(seconds=1000, fractional_seconds=300),
            PrecisionTimestamp(seconds=1001, fractional_seconds=400),
        ]
        waveform_proto = self.make_waveform_proto()
        waveform_proto.timestamps.extend(expected_timestamps)

        waveform = self.from_protobuf(waveform_proto)

        self._assert_waveform_irregular_timing_with_timestamps(waveform, expected_timestamps)

    def test___waveform_proto_with_t0_and_offset_no_timestamp___convert___raises_exception(
        self,
    ) -> None:
        """Test conversion of a waveform proto with t0 and offset, but no timestamp."""
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0.CopyFrom(t0_pt)
        waveform_proto.dt = 0.1
        waveform_proto.time_offset = 1.0

        with pytest.raises(ValueError):
            _ = self.from_protobuf(waveform_proto)

    def _to_proto_timestamps(self, timestamps: list[dt.datetime]) -> list[PrecisionTimestamp]:
        return [bintime_datetime_to_protobuf(bt.DateTime(ts)) for ts in timestamps]

    def _assert_proto_standard_timing(
        self,
        waveform_proto: AnyWaveformProto,
        t0_dt: dt.datetime,
        sample_interval: float,
    ) -> None:
        assert waveform_proto.dt == sample_interval
        assert waveform_proto.t0 == bintime_datetime_to_protobuf(bt.DateTime(t0_dt))

    def _assert_proto_standard_timing_with_offset(
        self,
        waveform_proto: AnyWaveformProto,
        t0_dt: dt.datetime,
        time_offset: dt.timedelta,
        sample_interval: float,
    ) -> None:
        assert waveform_proto.dt == sample_interval
        assert waveform_proto.t0 == bintime_datetime_to_protobuf(bt.DateTime(t0_dt + time_offset))
        assert waveform_proto.HasField("timestamp")
        assert waveform_proto.timestamp == bintime_datetime_to_protobuf(bt.DateTime(t0_dt))
        assert waveform_proto.time_offset == pytest.approx(time_offset.total_seconds())

    def _assert_waveform_irregular_timing_with_timestamps(
        self,
        waveform: AnyNiWaveform,
        expected_timestamps: list[PrecisionTimestamp],
    ) -> None:
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.IRREGULAR
        actual_timestamps = waveform.timing.get_timestamps(0, waveform.sample_count)
        bintime_datetimes = [convert_datetime(bt.DateTime, ts) for ts in actual_timestamps]
        assert [
            bintime_datetime_to_protobuf(btdt) for btdt in bintime_datetimes
        ] == expected_timestamps

    def _assert_waveform_timestamp_and_t0_timing(
        self,
        waveform: AnyNiWaveform,
        t0_seconds: int,
        timestamp_seconds: int,
        sample_interval: float,
        time_offset: float,
    ) -> None:
        bt_timestamp = convert_datetime(bt.DateTime, waveform.timing.timestamp)
        bt_start_time = convert_datetime(bt.DateTime, waveform.timing.start_time)
        assert timestamp_seconds == bintime_datetime_to_protobuf(bt_timestamp).seconds
        assert not bintime_datetime_to_protobuf(bt_timestamp).fractional_seconds
        assert t0_seconds == bintime_datetime_to_protobuf(bt_start_time).seconds
        assert not bintime_datetime_to_protobuf(bt_start_time).fractional_seconds
        assert waveform.timing.sample_interval == ht.timedelta(seconds=sample_interval)
        assert waveform.timing.time_offset == ht.timedelta(seconds=time_offset)
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR

    def _normalize_precision_timestamp(self, timestamp: PrecisionTimestamp) -> PrecisionTimestamp:
        return PrecisionTimestamp() if timestamp is None else timestamp
