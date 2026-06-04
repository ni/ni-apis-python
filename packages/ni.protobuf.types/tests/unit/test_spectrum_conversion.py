import numpy as np
from nitypes.waveform import Spectrum

from ni.protobuf.types.waveform_conversion import (
    float64_spectrum_from_protobuf,
    float64_spectrum_to_protobuf,
)
from ni.protobuf.types.waveform_pb2 import (
    DoubleSpectrum,
    WaveformAttributeValue,
)


# ========================================================
# Spectrum to DoubleSpectrum
# ========================================================
def test___default_spectrum___convert___valid_protobuf() -> None:
    spectrum = Spectrum()

    dbl_spectrum = float64_spectrum_to_protobuf(spectrum)

    assert not dbl_spectrum.attributes
    assert spectrum.start_frequency == 0.0
    assert spectrum.frequency_increment == 0.0
    assert list(dbl_spectrum.data) == []


def test___spectrum_with_data___convert___valid_protobuf() -> None:
    spectrum = Spectrum.from_array_1d(np.array([1.0, 2.0, 3.0]))
    spectrum.start_frequency = 100.0
    spectrum.frequency_increment = 10.0

    dbl_spectrum = float64_spectrum_to_protobuf(spectrum)

    assert list(dbl_spectrum.data) == [1.0, 2.0, 3.0]
    assert dbl_spectrum.start_frequency == 100.0
    assert dbl_spectrum.frequency_increment == 10.0


def test___spectrum_with_extended_properties___convert___valid_protobuf() -> None:
    spectrum = Spectrum()
    spectrum.channel_name = "Dev1/ai0"
    spectrum.units = "Volts"

    dbl_spectrum = float64_spectrum_to_protobuf(spectrum)

    assert dbl_spectrum.attributes["NI_ChannelName"].string_value == "Dev1/ai0"
    assert dbl_spectrum.attributes["NI_UnitDescription"].string_value == "Volts"


# ========================================================
# DoubleSpectrum to Spectrum
# ========================================================
def test___default_dbl_spectrum___convert___valid_python_object() -> None:
    dbl_spectrum = DoubleSpectrum()

    spectrum = float64_spectrum_from_protobuf(dbl_spectrum)

    assert not spectrum.extended_properties
    assert spectrum.start_frequency == 0.0
    assert spectrum.frequency_increment == 0.0
    assert spectrum.sample_count == 0
    assert spectrum.data.size == 0


def test___dbl_spectrum_with_data___convert___valid_python_object() -> None:
    dbl_spectrum = DoubleSpectrum(
        data=[1.0, 2.0, 3.0], start_frequency=100.0, frequency_increment=10.0
    )

    spectrum = float64_spectrum_from_protobuf(dbl_spectrum)

    assert list(spectrum.data) == [1.0, 2.0, 3.0]
    assert spectrum.start_frequency == 100.0
    assert spectrum.frequency_increment == 10.0


def test___dbl_spectrum_with_attributes___convert___valid_python_object() -> None:
    attributes = {
        "NI_ChannelName": WaveformAttributeValue(string_value="Dev1/ai0"),
        "NI_UnitDescription": WaveformAttributeValue(string_value="Volts"),
    }
    dbl_spectrum = DoubleSpectrum(attributes=attributes)

    spectrum = float64_spectrum_from_protobuf(dbl_spectrum)

    assert spectrum.channel_name == "Dev1/ai0"
    assert spectrum.units == "Volts"
