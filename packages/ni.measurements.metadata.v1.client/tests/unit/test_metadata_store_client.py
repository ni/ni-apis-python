from unittest.mock import Mock

import grpc
import ni.measurements.metadata.v1.metadata_store_service_pb2 as metadata_store_service_types
import pytest
from ni.measurements.metadata.v1.metadata_store_service_pb2_grpc import (
    MetadataStoreServiceStub,
)
from pytest_mock import MockerFixture

from ni.measurements.metadata.v1.client import MetadataStoreClient


def test__get_dut__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetDutRequest()
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetDutResponse()
    stub_response.dut.serial_number = "123456"
    metadata_store_stub.GetDut.return_value = stub_response

    client_response = metadata_store_client.get_dut(client_request)

    metadata_store_stub.GetDut.assert_called_once()
    stub_request = metadata_store_stub.GetDut.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_duts__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryDutsRequest()
    client_request.odata_query = "serial_number eq '123456'"
    stub_response = metadata_store_service_types.QueryDutsResponse()
    dut1 = stub_response.duts.add()
    dut1.serial_number = "123456"
    metadata_store_stub.QueryDuts.return_value = stub_response

    client_response = metadata_store_client.query_duts(client_request)

    metadata_store_stub.QueryDuts.assert_called_once()
    stub_request = metadata_store_stub.QueryDuts.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_dut__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateDutRequest()
    client_request.dut.serial_number = "123456"
    stub_response = metadata_store_service_types.CreateDutResponse()
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateDut.return_value = stub_response

    client_response = metadata_store_client.create_dut(client_request)

    metadata_store_stub.CreateDut.assert_called_once()
    stub_request = metadata_store_stub.CreateDut.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_product__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetProductRequest()
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetProductResponse()
    stub_response.product.name = "Test Product"
    metadata_store_stub.GetProduct.return_value = stub_response

    client_response = metadata_store_client.get_product(client_request)

    metadata_store_stub.GetProduct.assert_called_once()
    stub_request = metadata_store_stub.GetProduct.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_products__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryProductsRequest()
    client_request.odata_query = "name eq 'Test Product'"
    stub_response = metadata_store_service_types.QueryProductsResponse()
    product1 = stub_response.products.add()
    product1.name = "Test Product"
    metadata_store_stub.QueryProducts.return_value = stub_response

    client_response = metadata_store_client.query_products(client_request)

    metadata_store_stub.QueryProducts.assert_called_once()
    stub_request = metadata_store_stub.QueryProducts.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_product__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateProductRequest()
    client_request.product.name = "Test Product"
    stub_response = metadata_store_service_types.CreateProductResponse()
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateProduct.return_value = stub_response

    client_response = metadata_store_client.create_product(client_request)

    metadata_store_stub.CreateProduct.assert_called_once()
    stub_request = metadata_store_stub.CreateProduct.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_operator__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetOperatorRequest()
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
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
    client_request.odata_query = "name eq 'Test Operator'"
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
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateOperator.return_value = stub_response

    client_response = metadata_store_client.create_operator(client_request)

    metadata_store_stub.CreateOperator.assert_called_once()
    stub_request = metadata_store_stub.CreateOperator.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_test_plan__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetTestPlanRequest()
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetTestPlanResponse()
    stub_response.test_plan.name = "Test Plan"
    metadata_store_stub.GetTestPlan.return_value = stub_response

    client_response = metadata_store_client.get_test_plan(client_request)

    metadata_store_stub.GetTestPlan.assert_called_once()
    stub_request = metadata_store_stub.GetTestPlan.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_test_plans__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryTestPlansRequest()
    client_request.odata_query = "name eq 'Test Plan'"
    stub_response = metadata_store_service_types.QueryTestPlansResponse()
    test_plan1 = stub_response.test_plans.add()
    test_plan1.name = "Test Plan"
    metadata_store_stub.QueryTestPlans.return_value = stub_response

    client_response = metadata_store_client.query_test_plans(client_request)

    metadata_store_stub.QueryTestPlans.assert_called_once()
    stub_request = metadata_store_stub.QueryTestPlans.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_test_plan__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateTestPlanRequest()
    client_request.test_plan.name = "Test Plan"
    stub_response = metadata_store_service_types.CreateTestPlanResponse()
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateTestPlan.return_value = stub_response

    client_response = metadata_store_client.create_test_plan(client_request)

    metadata_store_stub.CreateTestPlan.assert_called_once()
    stub_request = metadata_store_stub.CreateTestPlan.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_test__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetTestRequest()
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
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
    client_request.odata_query = "name eq 'Test'"
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
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
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
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
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
    client_request.odata_query = "name eq 'Test Station'"
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
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateTestStation.return_value = stub_response

    client_response = metadata_store_client.create_test_station(client_request)

    metadata_store_stub.CreateTestStation.assert_called_once()
    stub_request = metadata_store_stub.CreateTestStation.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_hardware__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetHardwareRequest()
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetHardwareResponse()
    stub_response.hardware.serial_number = "12345"
    metadata_store_stub.GetHardware.return_value = stub_response

    client_response = metadata_store_client.get_hardware(client_request)

    metadata_store_stub.GetHardware.assert_called_once()
    stub_request = metadata_store_stub.GetHardware.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_hardware__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryHardwareRequest()
    client_request.odata_query = "serial_number eq '12345'"
    stub_response = metadata_store_service_types.QueryHardwareResponse()
    hardware1 = stub_response.hardware.add()
    hardware1.serial_number = "12345"
    metadata_store_stub.QueryHardware.return_value = stub_response

    client_response = metadata_store_client.query_hardware(client_request)

    metadata_store_stub.QueryHardware.assert_called_once()
    stub_request = metadata_store_stub.QueryHardware.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_hardware__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateHardwareRequest()
    client_request.hardware.serial_number = "12345"
    stub_response = metadata_store_service_types.CreateHardwareResponse()
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateHardware.return_value = stub_response

    client_response = metadata_store_client.create_hardware(client_request)

    metadata_store_stub.CreateHardware.assert_called_once()
    stub_request = metadata_store_stub.CreateHardware.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__get_software__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.GetSoftwareRequest()
    client_request.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    stub_response = metadata_store_service_types.GetSoftwareResponse()
    stub_response.software.product = "Test Software"
    metadata_store_stub.GetSoftware.return_value = stub_response

    client_response = metadata_store_client.get_software(client_request)

    metadata_store_stub.GetSoftware.assert_called_once()
    stub_request = metadata_store_stub.GetSoftware.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_software__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QuerySoftwareRequest()
    client_request.odata_query = "product eq 'Test Software'"
    stub_response = metadata_store_service_types.QuerySoftwareResponse()
    software1 = stub_response.software.add()
    software1.product = "Test Software"
    metadata_store_stub.QuerySoftware.return_value = stub_response

    client_response = metadata_store_client.query_software(client_request)

    metadata_store_stub.QuerySoftware.assert_called_once()
    stub_request = metadata_store_stub.QuerySoftware.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__create_software__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.CreateSoftwareRequest()
    client_request.software.product = "Test Software"
    stub_response = metadata_store_service_types.CreateSoftwareResponse()
    stub_response.id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.CreateSoftware.return_value = stub_response

    client_response = metadata_store_client.create_software(client_request)

    metadata_store_stub.CreateSoftware.assert_called_once()
    stub_request = metadata_store_stub.CreateSoftware.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__register_metadata_schema__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.RegisterMetadataSchemaRequest()
    client_request.schema = "Schema Contents"
    stub_response = metadata_store_service_types.RegisterMetadataSchemaResponse()
    stub_response.schema_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.RegisterMetadataSchema.return_value = stub_response

    client_response = metadata_store_client.register_metadata_schema(client_request)

    metadata_store_stub.RegisterMetadataSchema.assert_called_once()
    stub_request = metadata_store_stub.RegisterMetadataSchema.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__enumerate_metadata_schemas__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.EnumerateMetadataSchemasRequest()
    stub_response = metadata_store_service_types.EnumerateMetadataSchemasResponse()
    schema1 = stub_response.schemas.add()
    schema1.schema = "Schema Contents"
    metadata_store_stub.EnumerateMetadataSchemas.return_value = stub_response

    client_response = metadata_store_client.enumerate_metadata_schemas(client_request)

    metadata_store_stub.EnumerateMetadataSchemas.assert_called_once()
    assert stub_response == client_response


def test__resolve_alias__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.ResolveAliasRequest()
    client_request.alias_name = "Test Alias"
    stub_response = metadata_store_service_types.ResolveAliasResponse()
    stub_response.alias.target_id = "6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.ResolveAlias.return_value = stub_response

    client_response = metadata_store_client.resolve_alias(client_request)

    metadata_store_stub.ResolveAlias.assert_called_once()
    stub_request = metadata_store_stub.ResolveAlias.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__query_aliases__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.QueryAliasesRequest()
    client_request.odata_query = "name eq 'test-alias'"
    stub_response = metadata_store_service_types.QueryAliasesResponse()
    alias1 = stub_response.aliases.add()
    alias1.name = "test-alias"
    metadata_store_stub.QueryAliases.return_value = stub_response

    client_response = metadata_store_client.query_aliases(client_request)

    metadata_store_stub.QueryAliases.assert_called_once()
    stub_request = metadata_store_stub.QueryAliases.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__register_alias__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.RegisterAliasRequest()
    client_request.alias_name = "test-alias"
    stub_response = metadata_store_service_types.RegisterAliasResponse()
    stub_response.alias.target_id = "ALIAS-6118CBCE-74A1-4DE8-9B3A-98DE34A3B837"
    metadata_store_stub.RegisterAlias.return_value = stub_response

    client_response = metadata_store_client.register_alias(client_request)

    metadata_store_stub.RegisterAlias.assert_called_once()
    stub_request = metadata_store_stub.RegisterAlias.call_args[0][0]
    assert stub_request == client_request
    assert stub_response == client_response


def test__unregister_alias__request_and_response_pass_through(
    metadata_store_client: MetadataStoreClient, metadata_store_stub: Mock
) -> None:
    client_request = metadata_store_service_types.UnregisterAliasRequest()
    client_request.alias_name = "test-alias"
    stub_response = metadata_store_service_types.UnregisterAliasResponse()
    stub_response.unregistered = True
    metadata_store_stub.UnregisterAlias.return_value = stub_response

    client_response = metadata_store_client.unregister_alias(client_request)

    metadata_store_stub.UnregisterAlias.assert_called_once()
    stub_request = metadata_store_stub.UnregisterAlias.call_args[0][0]
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
    stub.CreateDut = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateProduct = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateOperator = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateTestPlan = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateTest = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateTestStation = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateHardware = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.CreateSoftware = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetDut = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetProduct = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetOperator = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetTestPlan = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetTest = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetTestStation = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetHardware = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.GetSoftware = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryDuts = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryProducts = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryOperators = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryTestPlans = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryTests = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryTestStations = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryHardware = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QuerySoftware = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.RegisterMetadataSchema = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.EnumerateMetadataSchemas = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.ResolveAlias = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.QueryAliases = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.RegisterAlias = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    stub.UnregisterAlias = mocker.create_autospec(grpc.UnaryUnaryMultiCallable)
    return stub
