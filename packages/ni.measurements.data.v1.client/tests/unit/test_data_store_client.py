from unittest.mock import Mock

import grpc
import ni.measurements.data.v1.data_store_service_pb2 as data_store_service_types
import pytest
from ni.measurements.data.v1.data_store_service_pb2_grpc import (
    DataStoreServiceStub,
)
from pytest_mock import MockerFixture

from ni.measurements.data.v1.client import DataStoreClient


def test__create_session__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.CreateSessionRequest()
    client_request.session_metadata.session_name = "Test Session"
    stub_response = data_store_service_types.CreateSessionResponse()
    stub_response.session_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    data_store_stub.CreateSession.return_value = stub_response

    client_response = data_store_client.create_session(client_request)

    data_store_stub.CreateSession.assert_called_once()
    stub_request = data_store_stub.CreateSession.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_session__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.GetSessionRequest()
    client_request.session_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.GetSessionResponse()
    stub_response.session_metadata.session_name = "Test Session"
    data_store_stub.GetSession.return_value = stub_response

    client_response = data_store_client.get_session(client_request)

    data_store_stub.GetSession.assert_called_once()
    stub_request = data_store_stub.GetSession.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_measurement__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.CreateMeasurementRequest()
    client_request.measurement.name = "Test Measurement"
    stub_response = data_store_service_types.CreateMeasurementResponse()
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    data_store_stub.CreateMeasurement.return_value = stub_response

    client_response = data_store_client.create_measurement(client_request)

    data_store_stub.CreateMeasurement.assert_called_once()
    stub_request = data_store_stub.CreateMeasurement.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_measurement__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.GetMeasurementRequest()
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.GetMeasurementResponse()
    stub_response.measurement.name = "Test Measurement"
    data_store_stub.GetMeasurement.return_value = stub_response

    client_response = data_store_client.get_measurement(client_request)

    data_store_stub.GetMeasurement.assert_called_once()
    stub_request = data_store_stub.GetMeasurement.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_measurements__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.QueryMeasurementsRequest()
    client_request.odata_query = "name eq 'Test Measurement'"
    stub_response = data_store_service_types.QueryMeasurementsResponse()
    measurement1 = stub_response.measurements.add()
    measurement1.name = "Test Measurement"
    data_store_stub.QueryMeasurements.return_value = stub_response

    client_response = data_store_client.query_measurements(client_request)

    data_store_stub.QueryMeasurements.assert_called_once()
    stub_request = data_store_stub.QueryMeasurements.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_condition_set__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishConditionSetRequest()
    client_request.measurement_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    condition = client_request.condition_set.add()
    condition.name = "Temperature"
    stub_response = data_store_service_types.PublishConditionSetResponse()
    stub_response.stored_condition_set_value.moniker.service_location = "location"
    data_store_stub.PublishConditionSet.return_value = stub_response

    client_response = data_store_client.publish_condition_set(client_request)

    data_store_stub.PublishConditionSet.assert_called_once()
    stub_request = data_store_stub.PublishConditionSet.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_condition__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishConditionRequest()
    client_request.measurement_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishConditionResponse()
    stub_response.stored_condition_value.moniker.service_location = "location"
    data_store_stub.PublishCondition.return_value = stub_response

    client_response = data_store_client.publish_condition(client_request)

    data_store_stub.PublishCondition.assert_called_once()
    stub_request = data_store_stub.PublishCondition.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_condition_set_batch__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishConditionSetBatchRequest()
    client_request.measurement_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishConditionSetBatchResponse()
    stub_response.stored_condition_set_value.moniker.service_location = "location"
    data_store_stub.PublishConditionSetBatch.return_value = stub_response

    client_response = data_store_client.publish_condition_set_batch(client_request)

    data_store_stub.PublishConditionSetBatch.assert_called_once()
    stub_request = data_store_stub.PublishConditionSetBatch.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_condition_batch__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishConditionBatchRequest()
    client_request.measurement_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishConditionBatchResponse()
    data_store_stub.PublishConditionBatch.return_value = stub_response
    stub_response.stored_condition_value.moniker.service_location = "location"

    client_response = data_store_client.publish_condition_batch(client_request)

    data_store_stub.PublishConditionBatch.assert_called_once()
    stub_request = data_store_stub.PublishConditionBatch.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_data__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishDataRequest()
    client_request.measurement_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishDataResponse()
    data_store_stub.PublishData.return_value = stub_response
    stub_response.stored_data_value.moniker.service_location = "location"

    client_response = data_store_client.publish_data(client_request)

    data_store_stub.PublishData.assert_called_once()
    stub_request = data_store_stub.PublishData.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_data_batch__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishDataBatchRequest()
    client_request.measurement_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishDataBatchResponse()
    data_store_stub.PublishDataBatch.return_value = stub_response
    data_value = stub_response.stored_data_values.add()
    data_value.moniker.service_location = "location"

    client_response = data_store_client.publish_data_batch(client_request)

    data_store_stub.PublishDataBatch.assert_called_once()
    stub_request = data_store_stub.PublishDataBatch.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_condition_sets__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.QueryConditionSetsRequest()
    client_request.odata_query = "name eq 'Temperature'"
    stub_response = data_store_service_types.QueryConditionSetsResponse()
    condition_set = stub_response.stored_condition_set_values.add()
    condition_set.moniker.service_location = "location"
    data_store_stub.QueryConditionSets.return_value = stub_response

    client_response = data_store_client.query_condition_sets(client_request)

    data_store_stub.QueryConditionSets.assert_called_once()
    stub_request = data_store_stub.QueryConditionSets.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_conditions__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.QueryConditionsRequest()
    client_request.odata_query = "name eq 'Temperature'"
    stub_response = data_store_service_types.QueryConditionsResponse()
    condition = stub_response.stored_condition_values.add()
    condition.moniker.service_location = "location"
    data_store_stub.QueryConditions.return_value = stub_response

    client_response = data_store_client.query_conditions(client_request)

    data_store_stub.QueryConditions.assert_called_once()
    stub_request = data_store_stub.QueryConditions.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_data__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.QueryDataRequest()
    client_request.odata_query = "name eq 'Test Data'"
    stub_response = data_store_service_types.QueryDataResponse()
    data_value = stub_response.stored_data_values.add()
    data_value.moniker.service_location = "location"
    data_store_stub.QueryData.return_value = stub_response

    client_response = data_store_client.query_data(client_request)

    data_store_stub.QueryData.assert_called_once()
    stub_request = data_store_stub.QueryData.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


@pytest.fixture
def data_store_client(
    mocker: MockerFixture,
    data_store_stub: Mock,
) -> DataStoreClient:
    """Create a Client with a mock DataStoreServiceStub."""
    mocker.patch(
        "ni.measurements.data.v1.client.DataStoreClient._get_stub",
        return_value=data_store_stub,
    )
    client = DataStoreClient()
    return client


@pytest.fixture
def data_store_stub(mocker: MockerFixture) -> Mock:
    """Create a mock DataStoreServiceStub."""
    stub = mocker.create_autospec(DataStoreServiceStub)
    stub.CreateSession = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetSession = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateMeasurement = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetMeasurement = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryMeasurements = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishConditionSet = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishCondition = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishConditionSetBatch = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishConditionBatch = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishData = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishDataBatch = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryConditionSets = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryConditions = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryData = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    return stub
