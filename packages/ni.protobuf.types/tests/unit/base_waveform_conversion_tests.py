"""Unit tests for conversion of the timing aspects of various types of waveforms."""

import datetime as dt
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import runtime_checkable, Any, Generic, Protocol, TypeVar

import hightime as ht
import nitypes.bintime as bt
import pytest
from nitypes.time import convert_datetime
from nitypes.waveform import (
    AnalogWaveform,
    ComplexWaveform,
    DigitalWaveform,
    LinearScaleMode,
    NoneScaleMode,
    SampleIntervalMode,
    ScaleMode,
    Timing,
)

from ni.protobuf.types.precision_timestamp_conversion import (
    bintime_datetime_to_protobuf,
)
from ni.protobuf.types.precision_timestamp_pb2 import PrecisionTimestamp
from ni.protobuf.types.waveform_pb2 import (
    DigitalWaveform as DigitalWaveformProto,
    DoubleAnalogWaveform,
    DoubleComplexWaveform,
    I16AnalogWaveform,
    I16ComplexWaveform,
    LinearScale,
    Scale,
    WaveformAttributeValue,
)

TWaveform = TypeVar(
    "TWaveform", bound=AnalogWaveform[Any] | ComplexWaveform[Any] | DigitalWaveform[Any]
)
TWaveformProto = TypeVar(
    "TWaveformProto",
    DoubleAnalogWaveform,
    DoubleComplexWaveform,
    I16AnalogWaveform,
    I16ComplexWaveform,
    DigitalWaveformProto,
)


# ========================================================
# Base class
# ========================================================
class BaseWaveformConversionTests(ABC, Generic[TWaveform, TWaveformProto]):
    """Base class for testing waveform conversion.

    Subclasses implement more specific or typed waveform conversion tests.
    """

    @abstractmethod
    def make_waveform(self) -> TWaveform:
        """Create a waveform with small non-zero sample data."""
        ...

    @abstractmethod
    def make_waveform_proto(
        self,
        attributes: Mapping[str, WaveformAttributeValue] | None = None,
        scale: Scale | None = None,
    ) -> TWaveformProto:
        """Create a waveform protobuf object with small non-zero sample data."""
        ...

    @abstractmethod
    def to_protobuf(self, waveform: TWaveform) -> TWaveformProto:
        """Convert a Python waveform to its corresponding proto message."""
        ...

    @abstractmethod
    def from_protobuf(self, waveform_proto: TWaveformProto) -> TWaveform:
        """Convert a proto message to the corresponding Python waveform."""
        ...

    # ========================================================
    # To Protobuf
    # ========================================================
    def test___waveform_with_standard_timing___convert___valid_protobuf(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        sample_interval_seconds = 1.5
        waveform.timing = Timing.create_with_regular_interval(
            sample_interval=dt.timedelta(seconds=sample_interval_seconds),
            timestamp=t0_dt,
        )

        waveform_proto = self.to_protobuf(waveform)

        self._assert_proto_standard_timing(waveform_proto, t0_dt, sample_interval_seconds)

    def test___waveform_with_standard_timing_and_offset___convert___valid_protobuf(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
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

    def test___waveform_with_standard_timing___round_trip___waveforms_match(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
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

    def test___waveform_with_irregular_timing___convert___valid_protobuf(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
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
    def test___waveform_with_regular_timing___round_trip___waveforms_match(  # noqa D102: Missing docstring in public method
        self, timestamp_seconds: float, time_offset: float
    ) -> None:
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
        if isinstance(waveform, SupportsScaleMode):
            waveform.scale_mode = NoneScaleMode()

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
    def test___waveform_with_none_timing___round_trip___waveforms_match(  # noqa D102: Missing docstring in public method
        self, timestamp_seconds: int, time_offset: float
    ) -> None:
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
        if isinstance(waveform, SupportsScaleMode):
            waveform.scale_mode = NoneScaleMode()

        waveform_proto = self.to_protobuf(waveform)
        converted_waveform = self.from_protobuf(waveform_proto)

        assert waveform == converted_waveform

    def test___waveform_with_extended_properties___convert___valid_protobuf(self) -> None:  # noqa D102: Missing docstring in public method
        waveform = self.make_waveform()
        waveform.extended_properties["NI_ChannelName"] = "Dev1/ai0"
        waveform.extended_properties["NI_UnitDescription"] = "Volts"

        dbl_analog_waveform = self.to_protobuf(waveform)

        assert dbl_analog_waveform.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
        assert dbl_analog_waveform.attributes["NI_UnitDescription"].string_value == "Volts"

    def test____waveform_with_scaling___convert___valid_protobuf(self) -> None:  # noqa D102: Missing docstring in public method
        scale_mode = LinearScaleMode(2.0, 3.0)
        waveform = self.make_waveform()
        waveform_with_scale_mode = waveform  # Use a second variable to get around mypy issue.
        if not isinstance(waveform_with_scale_mode, SupportsScaleMode):
            pytest.skip("Waveform type does not support scaling")
        waveform_with_scale_mode.scale_mode = scale_mode

        waveform_proto = self.to_protobuf(waveform)

        # The SupportsScaleMode check above is not sufficient since some waveform converters
        # don't set the scale even though the original waveform has a scale_mode. An example
        # of this is AnalogWaveform[np.float64] -> DoubleAnalogWaveform. So I added a second
        # check before accessing waveform_proto.scale.
        if not isinstance(waveform_proto, SupportsScale):
            pytest.skip("Waveform type does not support scaling")
        assert waveform_proto.scale.linear_scale.gain == 2.0
        assert waveform_proto.scale.linear_scale.offset == 3.0

    # ========================================================
    # From Protobuf
    # ========================================================
    def test___waveform_proto_with_timing___convert___valid_python_object(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
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

    def test___waveform_proto_with_timing___round_trip___waveforms_match(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
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
    def test___waveform_proto_regular_timing___round_trip___timing_equivalent(  # noqa D102: Missing docstring in public method
        self,
        timestamp_seconds: int,
        start_time_seconds: int,
        offset: float,
        normalized_timestamp_seconds: int,
        normalized_start_time_seconds: int,
    ) -> None:
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

    def test___waveform_proto_with_timing_no_t0___convert___valid_python_object(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
        waveform_proto = self.make_waveform_proto()
        waveform_proto.dt = 0.1

        waveform = self.from_protobuf(waveform_proto)

        assert not waveform.timing.has_start_time
        assert waveform.timing.sample_interval == ht.timedelta(seconds=0.1)
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR

    def test___waveform_proto_with_timing_no_dt___convert___valid_python_object(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0.CopyFrom(t0_pt)

        waveform = self.from_protobuf(waveform_proto)

        assert waveform.timing.start_time == t0_dt._to_datetime_datetime()
        assert not waveform.timing.has_sample_interval
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.NONE

    def test___waveform_proto_with_dt_and_offset___convert___valid_python_object(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
        waveform_proto = self.make_waveform_proto()
        waveform_proto.dt = 0.1
        waveform_proto.time_offset = 1.5

        waveform = self.from_protobuf(waveform_proto)

        assert not waveform.timing.has_timestamp
        assert waveform.timing.sample_interval == ht.timedelta(seconds=0.1)
        assert waveform.timing.time_offset == ht.timedelta(seconds=1.5)
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR

    def test___waveform_proto_with_t0_and_timestamp_and_offset___convert___valid_python_object(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
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

    def test___waveform_proto_with_timestamps___convert___valid_python_object(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
        expected_timestamps = [
            PrecisionTimestamp(seconds=1000, fractional_seconds=300),
            PrecisionTimestamp(seconds=1001, fractional_seconds=400),
        ]
        waveform_proto = self.make_waveform_proto()
        waveform_proto.timestamps.extend(expected_timestamps)

        waveform = self.from_protobuf(waveform_proto)

        self._assert_waveform_irregular_timing_with_timestamps(waveform, expected_timestamps)

    def test___waveform_proto_with_t0_and_offset_no_timestamp___convert___raises_exception(  # noqa D102: Missing docstring in public method
        self,
    ) -> None:
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0.CopyFrom(t0_pt)
        waveform_proto.dt = 0.1
        waveform_proto.time_offset = 1.0

        with pytest.raises(ValueError):
            _ = self.from_protobuf(waveform_proto)

    def test___waveform_proto_with_attributes___convert___valid_python_object(self) -> None:  # noqa D102: Missing docstring in public method
        attributes = {
            "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
            "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
        }
        waveform_proto = self.make_waveform_proto(attributes=attributes)

        waveform = self.from_protobuf(waveform_proto)

        assert waveform.extended_properties["NI_ChannelName"] == "Dev1/ai0"
        assert waveform.extended_properties["NI_UnitDescription"] == "Volts"

    def test___waveform_proto_with_scaling___convert___valid_python_object(self) -> None:  # noqa D102: Missing docstring in public method
        linear_scale = LinearScale(gain=2.0, offset=3.0)
        scale = Scale(linear_scale=linear_scale)
        waveform_proto = self.make_waveform_proto(scale=scale)
        if not isinstance(waveform_proto, SupportsScale):
            pytest.skip("Waveform type does not support scaling")

        waveform = self.from_protobuf(waveform_proto)

        assert isinstance(waveform.scale_mode, LinearScaleMode)
        assert waveform.scale_mode.gain == 2.0
        assert waveform.scale_mode.offset == 3.0

    def _to_proto_timestamps(self, timestamps: list[dt.datetime]) -> list[PrecisionTimestamp]:
        return [bintime_datetime_to_protobuf(bt.DateTime(ts)) for ts in timestamps]

    def _assert_proto_standard_timing(
        self,
        waveform_proto: TWaveformProto,
        t0_dt: dt.datetime,
        sample_interval: float,
    ) -> None:
        assert waveform_proto.dt == sample_interval
        assert waveform_proto.t0 == bintime_datetime_to_protobuf(bt.DateTime(t0_dt))

    def _assert_proto_standard_timing_with_offset(
        self,
        waveform_proto: TWaveformProto,
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
        waveform: TWaveform,
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
        waveform: TWaveform,
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


@runtime_checkable
class SupportsScaleMode(Protocol):
    """A protocol to test if something has the scale_mode property."""
    @property
    def scale_mode(self) -> ScaleMode:
        """The scale mode."""
        ...

    @scale_mode.setter
    def scale_mode(self, value: ScaleMode) -> None:
         """The scale mode setter."""
         ...


@runtime_checkable
class SupportsScale(Protocol):
    """A protocol to test if something has the scale property."""
    @property
    def scale(self) -> Scale:
        """The scale."""
        ...

    @scale.setter
    def scale(self, value: Scale) -> None:
         """The scale setter."""
         ...
