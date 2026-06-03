from collections.abc import Mapping
from typing import Any

import hightime as ht
import numpy as np
from nitypes.complex import ComplexInt32Base, ComplexInt32DType
from nitypes.waveform import (
    AnalogWaveform,
    ComplexWaveform,
    DigitalWaveform,
    NoneScaleMode,
    SampleIntervalMode,
)

from ni.protobuf.types.waveform_conversion import (
    digital_waveform_from_protobuf,
    digital_waveform_to_protobuf,
    float64_analog_waveform_from_protobuf,
    float64_analog_waveform_to_protobuf,
    float64_complex_waveform_from_protobuf,
    float64_complex_waveform_to_protobuf,
    int16_analog_waveform_from_protobuf,
    int16_analog_waveform_to_protobuf,
    int16_complex_waveform_from_protobuf,
    int16_complex_waveform_to_protobuf,
)
from ni.protobuf.types.waveform_pb2 import (
    DigitalWaveform as DigitalWaveformProto,
    DoubleAnalogWaveform,
    DoubleComplexWaveform,
    I16AnalogWaveform,
    I16ComplexWaveform,
    Scale,
    WaveformAttributeValue,
)
from tests.unit.timed_waveform_conversion_tests import TimedWaveformConversionTests


class TestDoubleAnalogConversion(
    TimedWaveformConversionTests[AnalogWaveform[np.float64], DoubleAnalogWaveform]
):
    """Test for converting double analog waveforms to/from protobuf messages."""

    def make_waveform(self) -> AnalogWaveform[np.float64]:
        """Create a waveform with small non-zero sample data."""
        return AnalogWaveform.from_array_1d(np.array([1.0, 2.0]))

    def make_waveform_proto(
        self,
        attributes: Mapping[str, WaveformAttributeValue] | None = None,
        scale: Scale | None = None,
    ) -> DoubleAnalogWaveform:
        """Create a waveform protobuf object with small non-zero sample data."""
        return DoubleAnalogWaveform(y_data=[1.0, 2.0], attributes=attributes)

    def to_protobuf(self, waveform: AnalogWaveform[np.float64]) -> DoubleAnalogWaveform:
        """Convert a Python waveform to its corresponding proto message."""
        return float64_analog_waveform_to_protobuf(waveform)

    def from_protobuf(self, waveform_proto: DoubleAnalogWaveform) -> AnalogWaveform[np.float64]:
        """Convert a proto message to the corresponding Python waveform."""
        return float64_analog_waveform_from_protobuf(waveform_proto)

    # ========================================================
    # To Protobuf
    # ========================================================
    def test___default_analog_waveform___convert___valid_protobuf(self) -> None:
        analog_waveform = AnalogWaveform()

        dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

        assert not dbl_analog_waveform.attributes
        assert dbl_analog_waveform.dt == 0
        assert not dbl_analog_waveform.HasField("t0")
        assert list(dbl_analog_waveform.y_data) == []

    def test___analog_waveform_samples_only___convert___valid_protobuf(self) -> None:
        analog_waveform = AnalogWaveform(5)

        dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

        assert list(dbl_analog_waveform.y_data) == [0.0, 0.0, 0.0, 0.0, 0.0]

    def test___analog_waveform_non_zero_samples___convert___valid_protobuf(self) -> None:
        analog_waveform = AnalogWaveform.from_array_1d(np.array([1.0, 2.0, 3.0]))

        dbl_analog_waveform = float64_analog_waveform_to_protobuf(analog_waveform)

        assert list(dbl_analog_waveform.y_data) == [1.0, 2.0, 3.0]

    # ========================================================
    # From Protobuf
    # ========================================================
    def test___default_dbl_analog_wfm___convert___valid_python_object(self) -> None:
        dbl_analog_wfm = DoubleAnalogWaveform()

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

        print(analog_waveform.timing)
        assert not analog_waveform.extended_properties
        assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE
        assert analog_waveform.timing.time_offset == ht.timedelta()
        assert analog_waveform.scaled_data.size == 0
        assert analog_waveform.scale_mode == NoneScaleMode()

    def test___dbl_analog_wfm_with_y_data___convert___valid_python_object(self) -> None:
        dbl_analog_wfm = DoubleAnalogWaveform(y_data=[1.0, 2.0, 3.0])

        analog_waveform = float64_analog_waveform_from_protobuf(dbl_analog_wfm)

        assert list(analog_waveform.scaled_data) == [1.0, 2.0, 3.0]


class TestDoubleComplexWaveformConversion(
    TimedWaveformConversionTests[ComplexWaveform[np.complex128], DoubleComplexWaveform]
):
    """Test for converting double complex waveforms to/from protobuf messages."""

    def make_waveform(self) -> ComplexWaveform[np.complex128]:
        """Create a waveform with small non-zero sample data."""
        return ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)

    def make_waveform_proto(
        self,
        attributes: Mapping[str, WaveformAttributeValue] | None = None,
        scale: Scale | None = None,
    ) -> DoubleComplexWaveform:
        """Create a waveform protobuf object with small non-zero sample data."""
        return DoubleComplexWaveform(y_data=[1.0, 2.0, 3.0, 4.0], attributes=attributes)

    def to_protobuf(self, waveform: ComplexWaveform[np.complex128]) -> DoubleComplexWaveform:
        """Convert a Python waveform to its corresponding proto message."""
        return float64_complex_waveform_to_protobuf(waveform)

    def from_protobuf(
        self, waveform_proto: DoubleComplexWaveform
    ) -> ComplexWaveform[np.complex128]:
        """Convert a proto message to the corresponding Python waveform."""
        return float64_complex_waveform_from_protobuf(waveform_proto)

    # ========================================================
    # To Protobuf
    # ========================================================
    def test___default_float64_complex_waveform___convert___valid_protobuf(self) -> None:
        complex_waveform = ComplexWaveform(0, np.complex128)

        dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

        assert not dbl_complex_waveform.attributes
        assert dbl_complex_waveform.dt == 0
        assert not dbl_complex_waveform.HasField("t0")
        assert list(dbl_complex_waveform.y_data) == []

    def test___float64_complex_waveform_samples_only___convert___valid_protobuf(self) -> None:
        complex_waveform = ComplexWaveform(2, np.complex128)

        dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

        # Interleaved real/imaginary data.
        assert list(dbl_complex_waveform.y_data) == [0.0, 0.0, 0.0, 0.0]

    def test___float64_complex_waveform_non_zero_samples___convert___valid_protobuf(self) -> None:
        complex_waveform = ComplexWaveform.from_array_1d([1.5 + 2.5j, 3.5 + 4.5j], np.complex128)

        dbl_complex_waveform = float64_complex_waveform_to_protobuf(complex_waveform)

        assert list(dbl_complex_waveform.y_data) == [1.5, 2.5, 3.5, 4.5]

    # ========================================================
    # From Protobuf
    # ========================================================
    def test___default_dbl_complex_wfm___convert___valid_python_object(self) -> None:
        dbl_complex_waveform = DoubleComplexWaveform()

        complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

        assert not complex_waveform.extended_properties
        assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE
        assert complex_waveform.timing.time_offset == ht.timedelta()
        assert complex_waveform.scaled_data.size == 0
        assert complex_waveform.scale_mode == NoneScaleMode()

    def test___dbl_complex_wfm_with_y_data___convert___valid_python_object(self) -> None:
        dbl_complex_waveform = DoubleComplexWaveform(y_data=[1.0, 2.0, 3.0, 4.0])

        complex_waveform = float64_complex_waveform_from_protobuf(dbl_complex_waveform)

        assert list(complex_waveform.scaled_data) == [1.0 + 2.0j, 3.0 + 4.0j]


class TestI16ComplexWaveformConversion(
    TimedWaveformConversionTests[ComplexWaveform[ComplexInt32Base], I16ComplexWaveform]
):
    """Test for converting int complex waveforms to/from protobuf messages."""

    def make_waveform(self) -> ComplexWaveform[ComplexInt32Base]:
        """Create a waveform with small non-zero sample data."""
        return ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)

    def make_waveform_proto(
        self,
        attributes: Mapping[str, WaveformAttributeValue] | None = None,
        scale: Scale | None = None,
    ) -> I16ComplexWaveform:
        """Create a waveform protobuf object with small non-zero sample data."""
        return I16ComplexWaveform(y_data=[1, 2, 3, 4], attributes=attributes, scale=scale)

    def to_protobuf(self, waveform: ComplexWaveform[ComplexInt32Base]) -> I16ComplexWaveform:
        """Convert a Python waveform to its corresponding proto message."""
        return int16_complex_waveform_to_protobuf(waveform)

    def from_protobuf(
        self, waveform_proto: I16ComplexWaveform
    ) -> ComplexWaveform[ComplexInt32Base]:
        """Convert a proto message to the corresponding Python waveform."""
        return int16_complex_waveform_from_protobuf(waveform_proto)

    # ========================================================
    # From Protobuf
    # ========================================================
    def test___default_int16_complex_waveform___convert___valid_protobuf(self) -> None:
        complex_waveform = ComplexWaveform(0, ComplexInt32DType)

        i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

        assert not i16_complex_waveform.attributes
        assert i16_complex_waveform.dt == 0
        assert not i16_complex_waveform.HasField("t0")
        assert not i16_complex_waveform.HasField("scale")
        assert list(i16_complex_waveform.y_data) == []

    def test___int16_complex_waveform_samples_only___convert___valid_protobuf(self) -> None:
        complex_waveform = ComplexWaveform(2, ComplexInt32DType)

        i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

        # Interleaved real/imaginary data.
        assert list(i16_complex_waveform.y_data) == [0, 0, 0, 0]

    def test___int16_complex_waveform_non_zero_samples___convert___valid_protobuf(self) -> None:
        complex_waveform = ComplexWaveform.from_array_1d([(1, 2), (3, 4)], ComplexInt32DType)

        i16_complex_waveform = int16_complex_waveform_to_protobuf(complex_waveform)

        assert list(i16_complex_waveform.y_data) == [1, 2, 3, 4]

    # ========================================================
    # From Protobuf
    # ========================================================
    def test___default_int16_complex_wfm___convert___valid_python_object(self) -> None:
        i16_complex_waveform = I16ComplexWaveform()

        complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

        assert not complex_waveform.extended_properties
        assert complex_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE
        assert complex_waveform.timing.time_offset == ht.timedelta()
        assert complex_waveform.scaled_data.size == 0
        assert complex_waveform.scale_mode == NoneScaleMode()

    def test___int16_complex_wfm_with_y_data___convert___valid_python_object(self) -> None:
        i16_complex_waveform = I16ComplexWaveform(y_data=[1, 2, 3, 4])

        complex_waveform = int16_complex_waveform_from_protobuf(i16_complex_waveform)

        expected_raw_data = np.array([(1, 2), (3, 4)], ComplexInt32DType)
        assert np.array_equal(complex_waveform.raw_data, expected_raw_data)


class TestI16AnalogWaveformConversion(
    TimedWaveformConversionTests[AnalogWaveform[np.int16], I16AnalogWaveform]
):
    """Test for converting int analog waveforms to/from protobuf messages."""

    def make_waveform(self) -> AnalogWaveform[np.int16]:
        """Create a waveform with small non-zero sample data."""
        return AnalogWaveform.from_array_1d(np.array([1, 2], dtype=np.int16))

    def make_waveform_proto(
        self,
        attributes: Mapping[str, WaveformAttributeValue] | None = None,
        scale: Scale | None = None,
    ) -> I16AnalogWaveform:
        """Create a waveform protobuf object with small non-zero sample data."""
        return I16AnalogWaveform(y_data=[1, 2], attributes=attributes, scale=scale)

    def to_protobuf(self, waveform: AnalogWaveform[np.int16]) -> I16AnalogWaveform:
        """Convert a Python waveform to its corresponding proto message."""
        return int16_analog_waveform_to_protobuf(waveform)

    def from_protobuf(self, waveform_proto: I16AnalogWaveform) -> AnalogWaveform[np.int16]:
        """Convert a proto message to the corresponding Python waveform."""
        return int16_analog_waveform_from_protobuf(waveform_proto)

    # ========================================================
    # To Protobuf
    # ========================================================
    def test___default_int16_analog_waveform___convert___valid_protobuf(self) -> None:
        analog_waveform = AnalogWaveform(0, np.int16)

        i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

        assert not i16_analog_waveform.attributes
        assert i16_analog_waveform.dt == 0
        assert not i16_analog_waveform.HasField("t0")
        assert not i16_analog_waveform.HasField("scale")
        assert list(i16_analog_waveform.y_data) == []

    def test___int16_analog_waveform_samples_only___convert___valid_protobuf(self) -> None:
        analog_waveform = AnalogWaveform(5, np.int16)

        i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

        assert list(i16_analog_waveform.y_data) == [0, 0, 0, 0, 0]

    def test___int16_analog_waveform_non_zero_samples___convert___valid_protobuf(self) -> None:
        analog_waveform = AnalogWaveform.from_array_1d(np.array([1, 2, 3], dtype=np.int16))

        i16_analog_waveform = int16_analog_waveform_to_protobuf(analog_waveform)

        assert list(i16_analog_waveform.y_data) == [1, 2, 3]

    # ========================================================
    # From Protobuf
    # ========================================================
    def test___default_i16_analog_wfm___convert___valid_python_object(self) -> None:
        i16_analog_wfm = I16AnalogWaveform()

        analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

        assert not analog_waveform.extended_properties
        assert analog_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE
        assert analog_waveform.timing.time_offset == ht.timedelta()
        assert analog_waveform.scaled_data.size == 0
        assert analog_waveform.scale_mode == NoneScaleMode()

    def test___i16_analog_wfm_with_y_data___convert___valid_python_object(self) -> None:
        i16_analog_wfm = I16AnalogWaveform(y_data=[1, 2, 3])

        analog_waveform = int16_analog_waveform_from_protobuf(i16_analog_wfm)

        expected_raw_data = np.array([1, 2, 3], dtype=np.int16)
        assert np.array_equal(analog_waveform.raw_data, expected_raw_data)


class TestDigitalWaveformConversion(
    TimedWaveformConversionTests[DigitalWaveform[Any], DigitalWaveformProto]
):
    """Test for converting digital waveforms to/from protobuf messages."""

    def make_waveform(self) -> DigitalWaveform[Any]:
        """Create a waveform with small non-zero sample data."""
        data = np.array([[0, 1, 3], [7, 5, 1]], dtype=np.uint8)
        return DigitalWaveform.from_lines(data, signal_count=3)

    def make_waveform_proto(
        self,
        attributes: Mapping[str, WaveformAttributeValue] | None = None,
        scale: Scale | None = None,
    ) -> DigitalWaveformProto:
        """Create a waveform protobuf object with small non-zero sample data."""
        data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
        return DigitalWaveformProto(y_data=data.tobytes(), signal_count=3, attributes=attributes)

    def to_protobuf(self, waveform: DigitalWaveform[Any]) -> DigitalWaveformProto:
        """Convert a Python waveform to its corresponding proto message."""
        return digital_waveform_to_protobuf(waveform)

    def from_protobuf(self, waveform_proto: DigitalWaveformProto) -> DigitalWaveform[Any]:
        """Convert a proto message to the corresponding Python waveform."""
        return digital_waveform_from_protobuf(waveform_proto)

    # ========================================================
    # To Protobuf
    # ========================================================
    def test___default_digital_waveform___convert___valid_protobuf(self) -> None:
        digital_waveform = DigitalWaveform()

        digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

        assert not digital_waveform_proto.attributes
        assert digital_waveform_proto.dt == 0
        assert not digital_waveform_proto.HasField("t0")
        assert digital_waveform_proto.y_data == b""
        assert digital_waveform_proto.signal_count == 1

    def test___digital_waveform_with_data___convert___valid_protobuf(self) -> None:
        data = np.array([[0, 1, 3], [7, 5, 1]], dtype=np.uint8)
        digital_waveform = DigitalWaveform.from_lines(data, signal_count=3)

        digital_waveform_proto = digital_waveform_to_protobuf(digital_waveform)

        assert digital_waveform_proto.y_data == b"\x00\x01\x03\x07\x05\x01"
        assert digital_waveform_proto.signal_count == 3

    # ========================================================
    # From Protobuf
    # ========================================================
    def test___default_digital_waveform_proto___convert___valid_python_object(self) -> None:
        digital_waveform_proto = DigitalWaveformProto(signal_count=1)

        digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

        assert not digital_waveform.extended_properties
        assert digital_waveform.timing.sample_interval_mode == SampleIntervalMode.NONE
        assert digital_waveform.timing.time_offset == ht.timedelta()
        assert digital_waveform.data.size == 0
        assert digital_waveform.signal_count == 1

    def test___digital_waveform_proto_with_data___convert___valid_python_object(self) -> None:
        data = np.array([[0, 1, 0], [1, 0, 1]], dtype=np.uint8)
        digital_waveform_proto = DigitalWaveformProto(y_data=data.tobytes(), signal_count=3)

        digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

        assert np.array_equal(digital_waveform.data, data)
        assert digital_waveform.signal_count == 3

    def test___digital_waveform_proto_with_attributes___convert___valid_python_object(self) -> None:
        attributes = {
            "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/port0"),
        }
        digital_waveform_proto = DigitalWaveformProto(attributes=attributes, signal_count=1)

        digital_waveform = digital_waveform_from_protobuf(digital_waveform_proto)

        assert digital_waveform.channel_name == "Dev1/port0"
