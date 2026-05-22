import datetime as dt
from abc import abstractmethod
from typing import Any

import hightime as ht
import nitypes.bintime as bt
import numpy as np
import pytest
from nitypes.complex import ComplexInt32DType
from nitypes.time import convert_datetime
from nitypes.waveform import (
    AnalogWaveform,
    ComplexWaveform,
    DigitalWaveform,
    LinearScaleMode,
    NoneScaleMode,
    SampleIntervalMode,
    Spectrum,
    Timing,
)

from ni.protobuf.types.precision_timestamp_conversion import (
    bintime_datetime_to_protobuf,
)
from ni.protobuf.types.precision_timestamp_pb2 import PrecisionTimestamp
from ni.protobuf.types.waveform_conversion import (
    AnyNiWaveform,
    AnyWaveformProto,
    digital_waveform_from_protobuf,
    digital_waveform_to_protobuf,
    float64_analog_waveform_from_protobuf,
    float64_analog_waveform_to_protobuf,
    float64_complex_waveform_from_protobuf,
    float64_complex_waveform_to_protobuf,
    float64_spectrum_from_protobuf,
    float64_spectrum_to_protobuf,
    int16_analog_waveform_from_protobuf,
    int16_analog_waveform_to_protobuf,
    int16_complex_waveform_from_protobuf,
    int16_complex_waveform_to_protobuf,
)
from ni.protobuf.types.waveform_pb2 import (
    DigitalWaveform as DigitalWaveformProto,
    DoubleAnalogWaveform,
    DoubleComplexWaveform,
    DoubleSpectrum,
    I16AnalogWaveform,
    I16ComplexWaveform,
    LinearScale,
    Scale,
    WaveformAttributeValue,
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
        assert [bintime_datetime_to_protobuf(btdt) for btdt in bintime_datetimes] == expected_timestamps


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

    # ========================================================
    # To Protobuf
    # ========================================================

    def test___waveform_with_standard_timing___convert___valid_protobuf(self) -> None:
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        waveform.timing = Timing.create_with_regular_interval(
            sample_interval=dt.timedelta(milliseconds=1500),
            timestamp=t0_dt,
        )

        waveform_proto = self.to_protobuf(waveform)

        self._assert_proto_standard_timing(waveform_proto, t0_dt, 1.5)

    def test___waveform_with_standard_timing_and_offset___convert___valid_protobuf(self) -> None:
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        sample_interval = dt.timedelta(milliseconds=1000)
        time_offset = dt.timedelta(milliseconds=1000)
        waveform.timing = Timing.create_with_regular_interval(
            sample_interval=sample_interval,
            timestamp=t0_dt,
            time_offset=time_offset,
        )

        waveform_proto = float64_analog_waveform_to_protobuf(waveform)

        self._assert_proto_standard_timing_with_offset(waveform_proto, t0_dt, time_offset, 1.0)


    def test___waveform_with_standard_timing___round_trip___waveforms_match(self) -> None:
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        sample_interval = dt.timedelta(milliseconds=1000)
        time_offset = dt.timedelta(milliseconds=1000)
        waveform.timing = Timing.create_with_regular_interval(
            sample_interval=sample_interval,
            timestamp=t0_dt,
            time_offset=time_offset,
        )

        waveform_proto = self.to_protobuf(waveform)
        converted_waveform = self.from_protobuf(waveform_proto)

        assert waveform == converted_waveform


    def test___waveform_with_irregular_timing___convert___valid_protobuf(self) -> None:
        waveform = self.make_waveform()
        t0_dt = dt.datetime(2000, 12, 1, tzinfo=dt.timezone.utc)
        timestamps = [
            t0_dt,
            t0_dt + dt.timedelta(milliseconds=1000),
            t0_dt + dt.timedelta(milliseconds=3000),
        ]
        waveform.timing = Timing.create_with_irregular_interval(timestamps)

        waveform_proto = self.to_protobuf(waveform)

        assert list(waveform_proto.timestamps) == self._to_proto_timestamps(timestamps)


    @pytest.mark.parametrize(
        "timestamp_seconds, time_offset",
        [
            (0, 0),
            (0, 10),
            (100, 10),
            (100, 0),
        ],
    )
    def test___waveform_with_regular_timing___round_trip___waveforms_match(
        self, timestamp_seconds: int, time_offset: float
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
        waveform.scale_mode = NoneScaleMode()

        waveform_proto = self.to_protobuf(waveform)
        converted_waveform = self.from_protobuf(waveform_proto)

        assert waveform == converted_waveform


    @pytest.mark.parametrize(
        "timestamp_seconds, time_offset",
        [
            (0, 0),
            (0, 10),
            (100, 10),
            (100, 0),
        ],
    )
    def test___waveform_with_none_timing___round_trip___waveforms_match(
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
        waveform.scale_mode = NoneScaleMode()

        waveform_proto = self.to_protobuf(waveform)
        converted_waveform = self.from_protobuf(waveform_proto)

        assert waveform == converted_waveform

    # ========================================================
    # From Protobuf
    # ========================================================

    def test___proto_with_timing___convert___valid_python_object(self) -> None:
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        waveform_proto = self.make_waveform_proto()
        waveform_proto.t0 = t0_pt
        waveform_proto.dt = 0.1

        waveform = self.from_protobuf(waveform_proto)

        assert waveform.timing.start_time == t0_dt._to_datetime_datetime()
        assert waveform.timing.sample_interval == ht.timedelta(seconds=0.1)
        assert waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


    def test___dbl_analog_wfm_with_timing___round_trip___waveforms_match(self) -> None:
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        dbl_analog_wfm = DoubleAnalogWaveform(
            t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0], timestamp=t0_pt, time_offset=0.0
        )

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)
        converted_dbl_analog_wfm = float64_analog_waveform_to_protobuf(analog_waveform)

        assert dbl_analog_wfm == converted_dbl_analog_wfm


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
    def test___dbl_analog_wfm_regular_timing___round_trip___timing_equivalent(
        self,
        timestamp_seconds: int,
        start_time_seconds: int,
        offset: float,
        normalized_timestamp_seconds: int,
        normalized_start_time_seconds: int,
    ) -> None:
        t0_pt = PrecisionTimestamp(seconds=start_time_seconds, fractional_seconds=0)
        timestamp_pt = PrecisionTimestamp(seconds=timestamp_seconds, fractional_seconds=0)
        dbl_analog_wfm = DoubleAnalogWaveform(
            t0=t0_pt,
            dt=0.1,
            y_data=[1.0, 2.0, 3.0],
            timestamp=timestamp_pt,
            time_offset=offset,
        )

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)
        converted_dbl_analog_wfm = float64_analog_waveform_to_protobuf(analog_waveform)

        assert (
            normalized_timestamp_seconds
            == self._normalize_precision_timestamp(converted_dbl_analog_wfm.timestamp).seconds
        )
        assert (
            normalized_start_time_seconds
            == self._normalize_precision_timestamp(converted_dbl_analog_wfm.t0).seconds
        )

    def test___dbl_analog_wfm_with_timing_no_t0___convert___valid_python_object(self) -> None:
        dbl_analog_wfm = DoubleAnalogWaveform(dt=0.1, y_data=[1.0, 2.0, 3.0])

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

        assert not analog_waveform.timing.has_start_time
        assert analog_waveform.timing.sample_interval == ht.timedelta(seconds=0.1)
        assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


    def test___dbl_analog_wfm_with_timing_no_dt___convert___valid_python_object(self) -> None:
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        dbl_analog_wfm = DoubleAnalogWaveform(t0=t0_pt, y_data=[1.0, 2.0, 3.0])

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

        assert analog_waveform.timing.start_time == t0_dt._to_datetime_datetime()
        assert not analog_waveform.timing.has_sample_interval
        assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE


    def test___dbl_analog_wfm_with_dt_and_offset___convert___valid_python_object(self) -> None:
        dbl_analog_wfm = DoubleAnalogWaveform(dt=0.1, y_data=[1.0, 2.0, 3.0], time_offset=1.0)

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

        assert not analog_waveform.timing.has_timestamp
        assert analog_waveform.timing.sample_interval == ht.timedelta(seconds=0.1)
        assert analog_waveform.timing.time_offset == ht.timedelta(seconds=1.0)
        assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.REGULAR


    def test___dbl_analog_wfm_with_t0_and_timestamp_and_offset___convert___valid_python_object(self) -> (
        None
    ):
        sample_interval = 0.1
        t0_seconds = 1000001
        t0_pt = PrecisionTimestamp(seconds=t0_seconds, fractional_seconds=0)
        timestamp_seconds = 1000000
        timestamp_pt = PrecisionTimestamp(seconds=timestamp_seconds, fractional_seconds=0)
        time_offset = 1.0
        dbl_analog_wfm = DoubleAnalogWaveform(
            t0=t0_pt,
            dt=0.1,
            y_data=[1.0, 2.0, 3.0],
            timestamp=timestamp_pt,
            time_offset=time_offset,
        )

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

        self._assert_waveform_timestamp_and_t0_timing(
            analog_waveform, t0_seconds, timestamp_seconds, sample_interval, time_offset
        )


    def test___dbl_analog_wfm_with_timestamps___convert___valid_python_object(self) -> None:
        expected_timestamps = [
            PrecisionTimestamp(seconds=1000, fractional_seconds=0),
            PrecisionTimestamp(seconds=1001, fractional_seconds=0),
        ]
        dbl_analog_wfm = DoubleAnalogWaveform(
            y_data=[1.0, 2.0],
            timestamps=expected_timestamps,
        )

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

        self._assert_waveform_irregular_timing_with_timestamps(analog_waveform, expected_timestamps)


    def test___dbl_analog_wfm_with_t0_and_offset_no_timestamp___convert___raises_exception(self) -> None:
        t0_dt = bt.DateTime(2020, 5, 5, tzinfo=dt.timezone.utc)
        t0_pt = bintime_datetime_to_protobuf(t0_dt)
        dbl_analog_wfm = DoubleAnalogWaveform(t0=t0_pt, dt=0.1, y_data=[1.0, 2.0, 3.0], time_offset=1.0)

        with pytest.raises(ValueError):
            _ = float64_analog_waveform_from_protobuf(dbl_analog_wfm)