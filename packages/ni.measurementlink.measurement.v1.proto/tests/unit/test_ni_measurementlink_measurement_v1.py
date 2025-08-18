"""Tests for the ni.measurementlink.measurement.v1.proto package."""

from ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    GetMetadataRequest,
    GetMetadataResponse,
    MeasurementDetails,
    MeasurementSignature,
)


def test___creategetmetadatarequest___message_created() -> None:
    request = GetMetadataRequest()
    assert request is not None


def test___creategetmetadataresponse___message_created() -> None:
    response = GetMetadataResponse()
    assert response is not None


def test___getmetadataresponse___with_measurementdetails___retrieved() -> None:
    response = GetMetadataResponse(
        measurement_details=MeasurementDetails(display_name="Test Name", version="1.2.3")
    )
    assert response.measurement_details.display_name == "Test Name"
    assert response.measurement_details.version == "1.2.3"


def test___getmetadataresponse___with_measurementsignature___retrieved() -> None:
    response = GetMetadataResponse(
        measurement_signature=MeasurementSignature(
            configuration_parameters_message_type="Test Message Type",
            outputs_message_type="Test Outputs Message Type",
        )
    )
    assert (
        response.measurement_signature.configuration_parameters_message_type == "Test Message Type"
    )
    assert response.measurement_signature.outputs_message_type == "Test Outputs Message Type"
