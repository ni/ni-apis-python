from unittest.mock import Mock

import grpc
import ni.measurements.data.v1.data_store_service_pb2 as data_store_service_types
import pytest
from ni.measurements.data.v1.data_store_service_pb2_grpc import (
    DataStoreServiceStub,
)
from pytest_mock import MockerFixture

from ni.measurements.data.v1.client import DataStoreClient


def test__create_test_result__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.CreateTestResultRequest()
    client_request.test_result.name = "Test Result"
    stub_response = data_store_service_types.CreateTestResultResponse()
    stub_response.test_result_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    data_store_stub.CreateTestResult.return_value = stub_response

    client_response = data_store_client.create_test_result(client_request)

    data_store_stub.CreateTestResult.assert_called_once()
    stub_request = data_store_stub.CreateTestResult.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_test_result__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.GetTestResultRequest()
    client_request.test_result_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.GetTestResultResponse()
    stub_response.test_result.name = "Test Result"
    data_store_stub.GetTestResult.return_value = stub_response

    client_response = data_store_client.get_test_result(client_request)

    data_store_stub.GetTestResult.assert_called_once()
    stub_request = data_store_stub.GetTestResult.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_test_results__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.QueryTestResultsRequest()
    stub_response = data_store_service_types.QueryTestResultsResponse()
    test_result1 = stub_response.test_results.add()
    test_result1.name = "Test Result"
    data_store_stub.QueryTestResults.return_value = stub_response

    client_response = data_store_client.query_test_results(client_request)

    data_store_stub.QueryTestResults.assert_called_once()
    stub_request = data_store_stub.QueryTestResults.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_step__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.CreateStepRequest()
    client_request.step.name = "Test Step"
    stub_response = data_store_service_types.CreateStepResponse()
    stub_response.step_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    data_store_stub.CreateStep.return_value = stub_response

    client_response = data_store_client.create_step(client_request)

    data_store_stub.CreateStep.assert_called_once()
    stub_request = data_store_stub.CreateStep.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_step__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.GetStepRequest()
    client_request.step_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.GetStepResponse()
    stub_response.step.name = "Test Step"
    data_store_stub.GetStep.return_value = stub_response

    client_response = data_store_client.get_step(client_request)

    data_store_stub.GetStep.assert_called_once()
    stub_request = data_store_stub.GetStep.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_steps__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.QueryStepsRequest()
    client_request.odata_query = "OData Query"
    stub_response = data_store_service_types.QueryStepsResponse()
    step1 = stub_response.steps.add()
    step1.name = "Test Step"
    data_store_stub.QuerySteps.return_value = stub_response

    client_response = data_store_client.query_steps(client_request)

    data_store_stub.QuerySteps.assert_called_once()
    stub_request = data_store_stub.QuerySteps.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_condition__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishConditionRequest()
    client_request.step_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishConditionResponse()
    stub_response.published_condition.moniker.service_location = "location"
    data_store_stub.PublishCondition.return_value = stub_response

    client_response = data_store_client.publish_condition(client_request)

    data_store_stub.PublishCondition.assert_called_once()
    stub_request = data_store_stub.PublishCondition.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_condition_batch__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishConditionBatchRequest()
    client_request.step_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishConditionBatchResponse()
    data_store_stub.PublishConditionBatch.return_value = stub_response
    stub_response.published_condition.moniker.service_location = "location"

    client_response = data_store_client.publish_condition_batch(client_request)

    data_store_stub.PublishConditionBatch.assert_called_once()
    stub_request = data_store_stub.PublishConditionBatch.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_measurement__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishMeasurementRequest()
    client_request.step_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishMeasurementResponse()
    data_store_stub.PublishMeasurement.return_value = stub_response
    stub_response.published_measurement.moniker.service_location = "location"

    client_response = data_store_client.publish_measurement(client_request)

    data_store_stub.PublishMeasurement.assert_called_once()
    stub_request = data_store_stub.PublishMeasurement.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__publish_measurement_batch__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.PublishMeasurementBatchRequest()
    client_request.step_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = data_store_service_types.PublishMeasurementBatchResponse()
    data_store_stub.PublishMeasurementBatch.return_value = stub_response
    measurement = stub_response.published_measurements.add()
    measurement.moniker.service_location = "location"

    client_response = data_store_client.publish_measurement_batch(client_request)

    data_store_stub.PublishMeasurementBatch.assert_called_once()
    stub_request = data_store_stub.PublishMeasurementBatch.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_conditions__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.QueryConditionsRequest()
    client_request.odata_query = "OData Query"
    stub_response = data_store_service_types.QueryConditionsResponse()
    condition = stub_response.published_conditions.add()
    condition.moniker.service_location = "location"
    data_store_stub.QueryConditions.return_value = stub_response

    client_response = data_store_client.query_conditions(client_request)

    data_store_stub.QueryConditions.assert_called_once()
    stub_request = data_store_stub.QueryConditions.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_measurements__request_and_response_pass_through(
    data_store_client: DataStoreClient, data_store_stub: Mock
) -> None:
    client_request = data_store_service_types.QueryMeasurementsRequest()
    client_request.odata_query = "OData Query"
    stub_response = data_store_service_types.QueryMeasurementsResponse()
    measurement = stub_response.published_measurements.add()
    measurement.moniker.service_location = "location"
    data_store_stub.QueryMeasurements.return_value = stub_response

    client_response = data_store_client.query_measurements(client_request)

    data_store_stub.QueryMeasurements.assert_called_once()
    stub_request = data_store_stub.QueryMeasurements.call_args[0][0]
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
    stub.CreateTestResult = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetTestResult = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryTestResults = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateStep = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetStep = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QuerySteps = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishCondition = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishConditionBatch = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishMeasurement = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.PublishMeasurementBatch = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryConditions = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryMeasurements = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    return stub
