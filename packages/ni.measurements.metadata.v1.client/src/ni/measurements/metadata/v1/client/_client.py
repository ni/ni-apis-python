"""Client for accessing the NI Metadata Store Service."""

from typing import Optional

import grpc
import ni.measurements.metadata.v1.metadata_store_service_pb2 as metadata_store_service_pb2
import ni.measurements.metadata.v1.metadata_store_service_pb2_grpc as metadata_store_service_pb2_grpc
from ni.measurementlink.discovery.v1.client import DiscoveryClient
from ni_grpc_extensions.channelpool import GrpcChannelPool

from ni.measurements.metadata.v1.client._client_base import GrpcServiceClientBase

GRPC_SERVICE_INTERFACE_NAME = "ni.measurements.metadata.v1.MetadataStoreService"


class MetadataStoreClient(GrpcServiceClientBase):
    """Client for accessing the NI Metadata Store Service."""

    def __init__(
        self,
        *,
        discovery_client: Optional[DiscoveryClient] = None,
        grpc_channel: Optional[grpc.Channel] = None,
        grpc_channel_pool: Optional[GrpcChannelPool] = None,
    ) -> None:
        """Initialize the Metadata Store Client.

        Args:
            discovery_client: An optional discovery client (recommended).

            grpc_channel: An optional metadata store gRPC channel.

            grpc_channel_pool: An optional gRPC channel pool (recommended).
        """
        super().__init__(
            discovery_client=discovery_client,
            grpc_channel=grpc_channel,
            grpc_channel_pool=grpc_channel_pool,
            service_interface_name=GRPC_SERVICE_INTERFACE_NAME,
            service_class="",
            stub_class=metadata_store_service_pb2_grpc.MetadataStoreServiceStub,
        )

    def get_dut(
        self, request: metadata_store_service_pb2.GetDutRequest
    ) -> metadata_store_service_pb2.GetDutResponse:
        """Gets the device under test associated with the identifier given in the request."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.GetDut(request)

    def query_duts(
        self, request: metadata_store_service_pb2.QueryDutsRequest
    ) -> metadata_store_service_pb2.QueryDutsResponse:
        """Perform an OData query on DUTs."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QueryDuts(request)

    def create_dut(
        self, request: metadata_store_service_pb2.CreateDutRequest
    ) -> metadata_store_service_pb2.CreateDutResponse:
        """Creates a new device under test in the metadata store."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.CreateDut(request)

    def get_product(
        self, request: metadata_store_service_pb2.GetProductRequest
    ) -> metadata_store_service_pb2.GetProductResponse:
        """Gets the product associated with the identifier given in the request."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.GetProduct(request)

    def query_products(
        self, request: metadata_store_service_pb2.QueryProductsRequest
    ) -> metadata_store_service_pb2.QueryProductsResponse:
        """Perform an OData query on products."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QueryProducts(request)

    def create_product(
        self, request: metadata_store_service_pb2.CreateProductRequest
    ) -> metadata_store_service_pb2.CreateProductResponse:
        """Creates a new product in the metadata store."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.CreateProduct(request)

    def get_operator(
        self, request: metadata_store_service_pb2.GetOperatorRequest
    ) -> metadata_store_service_pb2.GetOperatorResponse:
        """Gets the operator associated with the identifier given in the request."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.GetOperator(request)

    def query_operators(
        self, request: metadata_store_service_pb2.QueryOperatorsRequest
    ) -> metadata_store_service_pb2.QueryOperatorsResponse:
        """Perform an OData query on operators."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QueryOperators(request)

    def create_operator(
        self, request: metadata_store_service_pb2.CreateOperatorRequest
    ) -> metadata_store_service_pb2.CreateOperatorResponse:
        """Creates a new operator in the metadata store."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.CreateOperator(request)

    def get_test_plan(
        self, request: metadata_store_service_pb2.GetTestPlanRequest
    ) -> metadata_store_service_pb2.GetTestPlanResponse:
        """Gets the test plan associated with the identifier given in the request."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.GetTestPlan(request)

    def query_test_plans(
        self, request: metadata_store_service_pb2.QueryTestPlansRequest
    ) -> metadata_store_service_pb2.QueryTestPlansResponse:
        """Perform an OData query on test plans."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QueryTestPlans(request)

    def create_test_plan(
        self, request: metadata_store_service_pb2.CreateTestPlanRequest
    ) -> metadata_store_service_pb2.CreateTestPlanResponse:
        """Creates a new test plan in the metadata store."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.CreateTestPlan(request)

    def get_test(
        self, request: metadata_store_service_pb2.GetTestRequest
    ) -> metadata_store_service_pb2.GetTestResponse:
        """Gets the test associated with the identifier given in the request."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.GetTest(request)

    def query_tests(
        self, request: metadata_store_service_pb2.QueryTestsRequest
    ) -> metadata_store_service_pb2.QueryTestsResponse:
        """Perform an OData query on tests."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QueryTests(request)

    def create_test(
        self, request: metadata_store_service_pb2.CreateTestRequest
    ) -> metadata_store_service_pb2.CreateTestResponse:
        """Creates a new test in the metadata store."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.CreateTest(request)

    def get_test_station(
        self, request: metadata_store_service_pb2.GetTestStationRequest
    ) -> metadata_store_service_pb2.GetTestStationResponse:
        """Gets the test station associated with the identifier given in the request."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.GetTestStation(request)

    def query_test_stations(
        self, request: metadata_store_service_pb2.QueryTestStationsRequest
    ) -> metadata_store_service_pb2.QueryTestStationsResponse:
        """Perform an OData query on test stations."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QueryTestStations(request)

    def create_test_station(
        self, request: metadata_store_service_pb2.CreateTestStationRequest
    ) -> metadata_store_service_pb2.CreateTestStationResponse:
        """Creates a new test station in the metadata store."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.CreateTestStation(request)

    def get_hardware(
        self, request: metadata_store_service_pb2.GetHardwareRequest
    ) -> metadata_store_service_pb2.GetHardwareResponse:
        """Gets the hardware associated with the identifier given in the request."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.GetHardware(request)

    def query_hardware(
        self, request: metadata_store_service_pb2.QueryHardwareRequest
    ) -> metadata_store_service_pb2.QueryHardwareResponse:
        """Perform an OData query on hardware."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QueryHardware(request)

    def create_hardware(
        self, request: metadata_store_service_pb2.CreateHardwareRequest
    ) -> metadata_store_service_pb2.CreateHardwareResponse:
        """Creates new hardware in the metadata store."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.CreateHardware(request)

    def get_software(
        self, request: metadata_store_service_pb2.GetSoftwareRequest
    ) -> metadata_store_service_pb2.GetSoftwareResponse:
        """Gets the software associated with the identifier given in the request."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.GetSoftware(request)

    def query_software(
        self, request: metadata_store_service_pb2.QuerySoftwareRequest
    ) -> metadata_store_service_pb2.QuerySoftwareResponse:
        """Perform an OData query on software."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QuerySoftware(request)

    def create_software(
        self, request: metadata_store_service_pb2.CreateSoftwareRequest
    ) -> metadata_store_service_pb2.CreateSoftwareResponse:
        """Creates new software in the metadata store."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.CreateSoftware(request)

    def register_metadata_schema(
        self, request: metadata_store_service_pb2.RegisterMetadataSchemaRequest
    ) -> metadata_store_service_pb2.RegisterMetadataSchemaResponse:
        """Registers a metadata schema."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.RegisterMetadataSchema(request)

    def enumerate_metadata_schemas(
        self, request: metadata_store_service_pb2.EnumerateMetadataSchemasRequest
    ) -> metadata_store_service_pb2.EnumerateMetadataSchemasResponse:
        """Enumerate the metadata schemas that have been previously registered."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.EnumerateMetadataSchemas(request)

    def resolve_alias(
        self, request: metadata_store_service_pb2.ResolveAliasRequest
    ) -> metadata_store_service_pb2.ResolveAliasResponse:
        """Resolves a given alias to its target."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.ResolveAlias(request)

    def query_aliases(
        self, request: metadata_store_service_pb2.QueryAliasesRequest
    ) -> metadata_store_service_pb2.QueryAliasesResponse:
        """Perform an OData query on the registered aliases."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.QueryAliases(request)

    def register_alias(
        self, request: metadata_store_service_pb2.RegisterAliasRequest
    ) -> metadata_store_service_pb2.RegisterAliasResponse:
        """Registers an alias of the specified metadata.

        This alias can be used when creating other metadata or publishing.
        """
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.RegisterAlias(request)

    def unregister_alias(
        self, request: metadata_store_service_pb2.UnregisterAliasRequest
    ) -> metadata_store_service_pb2.UnregisterAliasResponse:
        """Removes a registered alias."""
        stub: metadata_store_service_pb2_grpc.MetadataStoreServiceStub = self._get_stub()  # type: ignore
        return stub.UnregisterAlias(request)
