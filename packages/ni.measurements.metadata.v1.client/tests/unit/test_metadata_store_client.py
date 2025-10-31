from unittest.mock import Mock

import grpc
import ni.measurements.metadata.v1.metadata_store_service_pb2 as metadata_store_service_types
import pytest
from ni.measurements.metadata.v1.metadata_store_service_pb2_grpc import (
    MetadataStoreServiceStub,
)
from pytest_mock import MockerFixture

from ni.measurements.metadata.v1.client import MetadataStoreClient


def test__get_uut_instance__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetUutInstanceRequest()
    client_request.uut_instance_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetUutInstanceResponse()
    stub_response.uut_instance.serial_number = "123456"
    metadata_store_stub.GetUutInstance.return_value = stub_response

    client_response = metadata_store_client.get_uut_instance(client_request)

    metadata_store_stub.GetUutInstance.assert_called_once()
    stub_request = metadata_store_stub.GetUutInstance.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_uut_instances__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryUutInstancesRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryUutInstancesResponse()
    uut_instance1 = stub_response.uut_instances.add()
    uut_instance1.serial_number = "123456"
    metadata_store_stub.QueryUutInstances.return_value = stub_response

    client_response = metadata_store_client.query_uut_instances(client_request)

    metadata_store_stub.QueryUutInstances.assert_called_once()
    stub_request = metadata_store_stub.QueryUutInstances.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_uut_instance__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateUutInstanceRequest()
    client_request.uut_instance.serial_number = "123456"
    stub_response = metadata_store_service_types.CreateUutInstanceResponse()
    stub_response.uut_instance_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateUutInstance.return_value = stub_response

    client_response = metadata_store_client.create_uut_instance(client_request)

    metadata_store_stub.CreateUutInstance.assert_called_once()
    stub_request = metadata_store_stub.CreateUutInstance.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_uut__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetUutRequest()
    client_request.uut_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetUutResponse()
    stub_response.uut.model_name = "Test UUT Model"
    metadata_store_stub.GetUut.return_value = stub_response

    client_response = metadata_store_client.get_uut(client_request)

    metadata_store_stub.GetUut.assert_called_once()
    stub_request = metadata_store_stub.GetUut.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_uuts__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryUutsRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryUutsResponse()
    uut1 = stub_response.uuts.add()
    uut1.model_name = "Test UUT Model"
    metadata_store_stub.QueryUuts.return_value = stub_response

    client_response = metadata_store_client.query_uuts(client_request)

    metadata_store_stub.QueryUuts.assert_called_once()
    stub_request = metadata_store_stub.QueryUuts.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_uut__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateUutRequest()
    client_request.uut.model_name = "Test UUT Model"
    stub_response = metadata_store_service_types.CreateUutResponse()
    stub_response.uut_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateUut.return_value = stub_response

    client_response = metadata_store_client.create_uut(client_request)

    metadata_store_stub.CreateUut.assert_called_once()
    stub_request = metadata_store_stub.CreateUut.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_operator__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetOperatorRequest()
    client_request.operator_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetOperatorResponse()
    stub_response.operator.name = "Test Operator"
    metadata_store_stub.GetOperator.return_value = stub_response

    client_response = metadata_store_client.get_operator(client_request)

    metadata_store_stub.GetOperator.assert_called_once()
    stub_request = metadata_store_stub.GetOperator.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_operators__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryOperatorsRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryOperatorsResponse()
    operator1 = stub_response.operators.add()
    operator1.name = "Test Operator"
    metadata_store_stub.QueryOperators.return_value = stub_response

    client_response = metadata_store_client.query_operators(client_request)

    metadata_store_stub.QueryOperators.assert_called_once()
    stub_request = metadata_store_stub.QueryOperators.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_operator__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateOperatorRequest()
    client_request.operator.name = "Test Operator"
    stub_response = metadata_store_service_types.CreateOperatorResponse()
    stub_response.operator_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateOperator.return_value = stub_response

    client_response = metadata_store_client.create_operator(client_request)

    metadata_store_stub.CreateOperator.assert_called_once()
    stub_request = metadata_store_stub.CreateOperator.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_test_description__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetTestDescriptionRequest()
    client_request.test_description_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetTestDescriptionResponse()
    stub_response.test_description.name = "Test Description"
    metadata_store_stub.GetTestDescription.return_value = stub_response

    client_response = metadata_store_client.get_test_description(client_request)

    metadata_store_stub.GetTestDescription.assert_called_once()
    stub_request = metadata_store_stub.GetTestDescription.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_test_descriptions__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryTestDescriptionsRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryTestDescriptionsResponse()
    test_description1 = stub_response.test_descriptions.add()
    test_description1.name = "Test Description"
    metadata_store_stub.QueryTestDescriptions.return_value = stub_response

    client_response = metadata_store_client.query_test_descriptions(client_request)

    metadata_store_stub.QueryTestDescriptions.assert_called_once()
    stub_request = metadata_store_stub.QueryTestDescriptions.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_test_description__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateTestDescriptionRequest()
    client_request.test_description.name = "Test Description"
    stub_response = metadata_store_service_types.CreateTestDescriptionResponse()
    stub_response.test_description_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateTestDescription.return_value = stub_response

    client_response = metadata_store_client.create_test_description(client_request)

    metadata_store_stub.CreateTestDescription.assert_called_once()
    stub_request = metadata_store_stub.CreateTestDescription.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_test__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetTestRequest()
    client_request.test_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetTestResponse()
    stub_response.test.name = "Test"
    metadata_store_stub.GetTest.return_value = stub_response

    client_response = metadata_store_client.get_test(client_request)

    metadata_store_stub.GetTest.assert_called_once()
    stub_request = metadata_store_stub.GetTest.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_tests__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryTestsRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryTestsResponse()
    test1 = stub_response.tests.add()
    test1.name = "Test"
    metadata_store_stub.QueryTests.return_value = stub_response

    client_response = metadata_store_client.query_tests(client_request)

    metadata_store_stub.QueryTests.assert_called_once()
    stub_request = metadata_store_stub.QueryTests.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_test__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateTestRequest()
    client_request.test.name = "Test"
    stub_response = metadata_store_service_types.CreateTestResponse()
    stub_response.test_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateTest.return_value = stub_response

    client_response = metadata_store_client.create_test(client_request)

    metadata_store_stub.CreateTest.assert_called_once()
    stub_request = metadata_store_stub.CreateTest.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_test_station__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetTestStationRequest()
    client_request.test_station_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetTestStationResponse()
    stub_response.test_station.name = "Test Station"
    metadata_store_stub.GetTestStation.return_value = stub_response

    client_response = metadata_store_client.get_test_station(client_request)

    metadata_store_stub.GetTestStation.assert_called_once()
    stub_request = metadata_store_stub.GetTestStation.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_test_stations__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryTestStationsRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryTestStationsResponse()
    test_station1 = stub_response.test_stations.add()
    test_station1.name = "Test Station"
    metadata_store_stub.QueryTestStations.return_value = stub_response

    client_response = metadata_store_client.query_test_stations(client_request)

    metadata_store_stub.QueryTestStations.assert_called_once()
    stub_request = metadata_store_stub.QueryTestStations.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_test_station__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateTestStationRequest()
    client_request.test_station.name = "Test Station"
    stub_response = metadata_store_service_types.CreateTestStationResponse()
    stub_response.test_station_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateTestStation.return_value = stub_response

    client_response = metadata_store_client.create_test_station(client_request)

    metadata_store_stub.CreateTestStation.assert_called_once()
    stub_request = metadata_store_stub.CreateTestStation.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_hardware_item__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetHardwareItemRequest()
    client_request.hardware_item_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetHardwareItemResponse()
    stub_response.hardware_item.serial_number = "12345"
    metadata_store_stub.GetHardwareItem.return_value = stub_response

    client_response = metadata_store_client.get_hardware_item(client_request)

    metadata_store_stub.GetHardwareItem.assert_called_once()
    stub_request = metadata_store_stub.GetHardwareItem.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_hardware_items__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryHardwareItemsRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryHardwareItemsResponse()
    hardware_item1 = stub_response.hardware_items.add()
    hardware_item1.serial_number = "12345"
    metadata_store_stub.QueryHardwareItems.return_value = stub_response

    client_response = metadata_store_client.query_hardware_items(client_request)

    metadata_store_stub.QueryHardwareItems.assert_called_once()
    stub_request = metadata_store_stub.QueryHardwareItems.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_hardware_item__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateHardwareItemRequest()
    client_request.hardware_item.serial_number = "12345"
    stub_response = metadata_store_service_types.CreateHardwareItemResponse()
    stub_response.hardware_item_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateHardwareItem.return_value = stub_response

    client_response = metadata_store_client.create_hardware_item(client_request)

    metadata_store_stub.CreateHardwareItem.assert_called_once()
    stub_request = metadata_store_stub.CreateHardwareItem.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_software_item__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetSoftwareItemRequest()
    client_request.software_item_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetSoftwareItemResponse()
    stub_response.software_item.product = "Test Software"
    metadata_store_stub.GetSoftwareItem.return_value = stub_response

    client_response = metadata_store_client.get_software_item(client_request)

    metadata_store_stub.GetSoftwareItem.assert_called_once()
    stub_request = metadata_store_stub.GetSoftwareItem.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_software_items__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QuerySoftwareItemsRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QuerySoftwareItemsResponse()
    software_item1 = stub_response.software_items.add()
    software_item1.product = "Test Software"
    metadata_store_stub.QuerySoftwareItems.return_value = stub_response

    client_response = metadata_store_client.query_software_items(client_request)

    metadata_store_stub.QuerySoftwareItems.assert_called_once()
    stub_request = metadata_store_stub.QuerySoftwareItems.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_software_item__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateSoftwareItemRequest()
    client_request.software_item.product = "Test Software"
    stub_response = metadata_store_service_types.CreateSoftwareItemResponse()
    stub_response.software_item_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateSoftwareItem.return_value = stub_response

    client_response = metadata_store_client.create_software_item(client_request)

    metadata_store_stub.CreateSoftwareItem.assert_called_once()
    stub_request = metadata_store_stub.CreateSoftwareItem.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_test_adapter__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetTestAdapterRequest()
    client_request.test_adapter_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetTestAdapterResponse()
    stub_response.test_adapter.name = "Test Adapter"
    metadata_store_stub.GetTestAdapter.return_value = stub_response

    client_response = metadata_store_client.get_test_adapter(client_request)

    metadata_store_stub.GetTestAdapter.assert_called_once()
    stub_request = metadata_store_stub.GetTestAdapter.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_test_adapters__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryTestAdaptersRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryTestAdaptersResponse()
    test_adapter1 = stub_response.test_adapters.add()
    test_adapter1.name = "Test Adapter"
    metadata_store_stub.QueryTestAdapters.return_value = stub_response

    client_response = metadata_store_client.query_test_adapters(client_request)

    metadata_store_stub.QueryTestAdapters.assert_called_once()
    stub_request = metadata_store_stub.QueryTestAdapters.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_test_adapter__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateTestAdapterRequest()
    client_request.test_adapter.name = "Test Adapter"
    stub_response = metadata_store_service_types.CreateTestAdapterResponse()
    stub_response.test_adapter_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateTestAdapter.return_value = stub_response

    client_response = metadata_store_client.create_test_adapter(client_request)

    metadata_store_stub.CreateTestAdapter.assert_called_once()
    stub_request = metadata_store_stub.CreateTestAdapter.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__register_schema__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.RegisterSchemaRequest()
    client_request.schema = "Schema Contents"
    stub_response = metadata_store_service_types.RegisterSchemaResponse()
    stub_response.schema_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.RegisterSchema.return_value = stub_response

    client_response = metadata_store_client.register_schema(client_request)

    metadata_store_stub.RegisterSchema.assert_called_once()
    stub_request = metadata_store_stub.RegisterSchema.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__list_schemas__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.ListSchemasRequest()
    stub_response = metadata_store_service_types.ListSchemasResponse()
    schema1 = stub_response.schemas.add()
    schema1.schema = "Schema Contents"
    metadata_store_stub.ListSchemas.return_value = stub_response

    client_response = metadata_store_client.list_schemas(client_request)

    metadata_store_stub.ListSchemas.assert_called_once()
    assert stub_response == client_response


def test__get_alias__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetAliasRequest()
    client_request.alias_name = "Test Alias"
    stub_response = metadata_store_service_types.GetAliasResponse()
    stub_response.alias.target_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.GetAlias.return_value = stub_response

    client_response = metadata_store_client.get_alias(client_request)

    metadata_store_stub.GetAlias.assert_called_once()
    stub_request = metadata_store_stub.GetAlias.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_aliases__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryAliasesRequest()
    client_request.odata_query = "OData Query"
    stub_response = metadata_store_service_types.QueryAliasesResponse()
    alias1 = stub_response.aliases.add()
    alias1.name = "test-alias"
    metadata_store_stub.QueryAliases.return_value = stub_response

    client_response = metadata_store_client.query_aliases(client_request)

    metadata_store_stub.QueryAliases.assert_called_once()
    stub_request = metadata_store_stub.QueryAliases.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_alias__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateAliasRequest()
    client_request.alias_name = "test-alias"
    stub_response = metadata_store_service_types.CreateAliasResponse()
    stub_response.alias.target_id = "ALIAS-6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateAlias.return_value = stub_response

    client_response = metadata_store_client.create_alias(client_request)

    metadata_store_stub.CreateAlias.assert_called_once()
    stub_request = metadata_store_stub.CreateAlias.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__delete_alias__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.DeleteAliasRequest()
    client_request.alias_name = "test-alias"
    stub_response = metadata_store_service_types.DeleteAliasResponse()
    stub_response.unregistered = True
    metadata_store_stub.DeleteAlias.return_value = stub_response

    client_response = metadata_store_client.delete_alias(client_request)

    metadata_store_stub.DeleteAlias.assert_called_once()
    stub_request = metadata_store_stub.DeleteAlias.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


@pytest.fixture
def metadata_store_client(
    mocker: MockerFixture,
    metadata_store_stub: Mock,
) -> MetadataStoreClient:
    """Create a Client with a mock MetadataStoreServiceStub."""
    mocker.patch(
        "ni.measurements.metadata.v1.client.MetadataStoreClient._get_stub",
        return_value=metadata_store_stub,
    )
    client = MetadataStoreClient()
    return client


@pytest.fixture
def metadata_store_stub(mocker: MockerFixture) -> Mock:
    """Create a mock MetadataStoreServiceStub."""
    stub = mocker.create_autospec(MetadataStoreServiceStub)
    stub.CreateUutInstance = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateUut = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateOperator = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateTestDescription = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateTest = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateTestStation = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateHardwareItem = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateSoftwareItem = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateTestAdapter = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetUutInstance = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetUut = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetOperator = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetTestDescription = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetTest = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetTestStation = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetHardwareItem = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetSoftwareItem = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetTestAdapter = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryUutInstances = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryUuts = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryOperators = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryTestDescriptions = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryTests = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryTestStations = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryHardwareItems = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QuerySoftwareItems = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryTestAdapters = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.RegisterSchema = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.ListSchemas = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetAlias = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryAliases = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateAlias = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.DeleteAlias = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    return stub
