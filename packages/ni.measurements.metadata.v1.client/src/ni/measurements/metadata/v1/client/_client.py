"""Client for accessing the NI Metadata Store Service."""

from __future__ import annotations

import grpc
from ni.measurementlink.discovery.v1.client import DiscoveryClient
from ni.measurements.metadata.v1 import (
    metadata_store_service_pb2,
    metadata_store_service_pb2_grpc,
)
from ni_grpc_extensions.channelpool import GrpcChannelPool

from ni.measurements.metadata.v1.client._client_base import GrpcServiceClientBase


class MetadataStoreClient(
    GrpcServiceClientBase[metadata_store_service_pb2_grpc.MetadataStoreServiceStub]
):
    """Client for accessing the NI Metadata Store Service."""

    __slots__ = ()

    def __init__(
        self,
        *,
        discovery_client: DiscoveryClient | None = None,
        grpc_channel: grpc.Channel | None = None,
        grpc_channel_pool: GrpcChannelPool | None = None,
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
            service_interface_name="ni.measurements.metadata.v1.MetadataStoreService",
            service_class="",
            stub_class=metadata_store_service_pb2_grpc.MetadataStoreServiceStub,
        )

    def get_uut_instance(
        self, request: metadata_store_service_pb2.GetUutInstanceRequest
    ) -> metadata_store_service_pb2.GetUutInstanceResponse:
        """Gets the UUT instance associated with the identifier given in the request."""
        return self._get_stub().GetUutInstance(request)

    def query_uut_instances(
        self, request: metadata_store_service_pb2.QueryUutInstancesRequest
    ) -> metadata_store_service_pb2.QueryUutInstancesResponse:
        """Perform an OData query on UUT instances."""
        return self._get_stub().QueryUutInstances(request)

    def create_uut_instance(
        self, request: metadata_store_service_pb2.CreateUutInstanceRequest
    ) -> metadata_store_service_pb2.CreateUutInstanceResponse:
        """Creates a new UUT instance in the metadata store."""
        return self._get_stub().CreateUutInstance(request)

    def get_uut(
        self, request: metadata_store_service_pb2.GetUutRequest
    ) -> metadata_store_service_pb2.GetUutResponse:
        """Gets the UUT associated with the identifier given in the request."""
        return self._get_stub().GetUut(request)

    def query_uuts(
        self, request: metadata_store_service_pb2.QueryUutsRequest
    ) -> metadata_store_service_pb2.QueryUutsResponse:
        """Perform an OData query on UUTs."""
        return self._get_stub().QueryUuts(request)

    def create_uut(
        self, request: metadata_store_service_pb2.CreateUutRequest
    ) -> metadata_store_service_pb2.CreateUutResponse:
        """Creates a new UUT in the metadata store."""
        return self._get_stub().CreateUut(request)

    def get_operator(
        self, request: metadata_store_service_pb2.GetOperatorRequest
    ) -> metadata_store_service_pb2.GetOperatorResponse:
        """Gets the operator associated with the identifier given in the request."""
        return self._get_stub().GetOperator(request)

    def query_operators(
        self, request: metadata_store_service_pb2.QueryOperatorsRequest
    ) -> metadata_store_service_pb2.QueryOperatorsResponse:
        """Perform an OData query on operators."""
        return self._get_stub().QueryOperators(request)

    def create_operator(
        self, request: metadata_store_service_pb2.CreateOperatorRequest
    ) -> metadata_store_service_pb2.CreateOperatorResponse:
        """Creates a new operator in the metadata store."""
        return self._get_stub().CreateOperator(request)

    def get_test_description(
        self, request: metadata_store_service_pb2.GetTestDescriptionRequest
    ) -> metadata_store_service_pb2.GetTestDescriptionResponse:
        """Gets the test description associated with the identifier given in the request."""
        return self._get_stub().GetTestDescription(request)

    def query_test_descriptions(
        self, request: metadata_store_service_pb2.QueryTestDescriptionsRequest
    ) -> metadata_store_service_pb2.QueryTestDescriptionsResponse:
        """Perform an OData query on test descriptions."""
        return self._get_stub().QueryTestDescriptions(request)

    def create_test_description(
        self, request: metadata_store_service_pb2.CreateTestDescriptionRequest
    ) -> metadata_store_service_pb2.CreateTestDescriptionResponse:
        """Creates a new test description in the metadata store."""
        return self._get_stub().CreateTestDescription(request)

    def get_test(
        self, request: metadata_store_service_pb2.GetTestRequest
    ) -> metadata_store_service_pb2.GetTestResponse:
        """Gets the test associated with the identifier given in the request."""
        return self._get_stub().GetTest(request)

    def query_tests(
        self, request: metadata_store_service_pb2.QueryTestsRequest
    ) -> metadata_store_service_pb2.QueryTestsResponse:
        """Perform an OData query on tests."""
        return self._get_stub().QueryTests(request)

    def create_test(
        self, request: metadata_store_service_pb2.CreateTestRequest
    ) -> metadata_store_service_pb2.CreateTestResponse:
        """Creates a new test in the metadata store."""
        return self._get_stub().CreateTest(request)

    def get_test_station(
        self, request: metadata_store_service_pb2.GetTestStationRequest
    ) -> metadata_store_service_pb2.GetTestStationResponse:
        """Gets the test station associated with the identifier given in the request."""
        return self._get_stub().GetTestStation(request)

    def query_test_stations(
        self, request: metadata_store_service_pb2.QueryTestStationsRequest
    ) -> metadata_store_service_pb2.QueryTestStationsResponse:
        """Perform an OData query on test stations."""
        return self._get_stub().QueryTestStations(request)

    def create_test_station(
        self, request: metadata_store_service_pb2.CreateTestStationRequest
    ) -> metadata_store_service_pb2.CreateTestStationResponse:
        """Creates a new test station in the metadata store."""
        return self._get_stub().CreateTestStation(request)

    def get_hardware_item(
        self, request: metadata_store_service_pb2.GetHardwareItemRequest
    ) -> metadata_store_service_pb2.GetHardwareItemResponse:
        """Gets the hardware item associated with the identifier given in the request."""
        return self._get_stub().GetHardwareItem(request)

    def query_hardware_items(
        self, request: metadata_store_service_pb2.QueryHardwareItemsRequest
    ) -> metadata_store_service_pb2.QueryHardwareItemsResponse:
        """Perform an OData query on hardware items."""
        return self._get_stub().QueryHardwareItems(request)

    def create_hardware_item(
        self, request: metadata_store_service_pb2.CreateHardwareItemRequest
    ) -> metadata_store_service_pb2.CreateHardwareItemResponse:
        """Creates a new hardware item in the metadata store."""
        return self._get_stub().CreateHardwareItem(request)

    def get_software_item(
        self, request: metadata_store_service_pb2.GetSoftwareItemRequest
    ) -> metadata_store_service_pb2.GetSoftwareItemResponse:
        """Gets the software item associated with the identifier given in the request."""
        return self._get_stub().GetSoftwareItem(request)

    def query_software_items(
        self, request: metadata_store_service_pb2.QuerySoftwareItemsRequest
    ) -> metadata_store_service_pb2.QuerySoftwareItemsResponse:
        """Perform an OData query on software items."""
        return self._get_stub().QuerySoftwareItems(request)

    def create_software_item(
        self, request: metadata_store_service_pb2.CreateSoftwareItemRequest
    ) -> metadata_store_service_pb2.CreateSoftwareItemResponse:
        """Creates a new software item in the metadata store."""
        return self._get_stub().CreateSoftwareItem(request)

    def get_test_adapter(
        self, request: metadata_store_service_pb2.GetTestAdapterRequest
    ) -> metadata_store_service_pb2.GetTestAdapterResponse:
        """Gets the test adapter associated with the identifier given in the request."""
        return self._get_stub().GetTestAdapter(request)

    def query_test_adapters(
        self, request: metadata_store_service_pb2.QueryTestAdaptersRequest
    ) -> metadata_store_service_pb2.QueryTestAdaptersResponse:
        """Perform an OData query on test adapters."""
        return self._get_stub().QueryTestAdapters(request)

    def create_test_adapter(
        self, request: metadata_store_service_pb2.CreateTestAdapterRequest
    ) -> metadata_store_service_pb2.CreateTestAdapterResponse:
        """Creates a new test adapter in the metadata store."""
        return self._get_stub().CreateTestAdapter(request)

    def register_schema(
        self, request: metadata_store_service_pb2.RegisterSchemaRequest
    ) -> metadata_store_service_pb2.RegisterSchemaResponse:
        """Registers a schema."""
        return self._get_stub().RegisterSchema(request)

    def list_schemas(
        self, request: metadata_store_service_pb2.ListSchemasRequest
    ) -> metadata_store_service_pb2.ListSchemasResponse:
        """List the schemas that have been previously registered."""
        return self._get_stub().ListSchemas(request)

    def get_alias(
        self, request: metadata_store_service_pb2.GetAliasRequest
    ) -> metadata_store_service_pb2.GetAliasResponse:
        """Gets the target of a given alias."""
        return self._get_stub().GetAlias(request)

    def query_aliases(
        self, request: metadata_store_service_pb2.QueryAliasesRequest
    ) -> metadata_store_service_pb2.QueryAliasesResponse:
        """Perform an OData query on the created aliases."""
        return self._get_stub().QueryAliases(request)

    def create_alias(
        self, request: metadata_store_service_pb2.CreateAliasRequest
    ) -> metadata_store_service_pb2.CreateAliasResponse:
        """Creates an alias of the specified metadata.

        This alias can be used when creating other metadata or publishing.
        """
        return self._get_stub().CreateAlias(request)

    def delete_alias(
        self, request: metadata_store_service_pb2.DeleteAliasRequest
    ) -> metadata_store_service_pb2.DeleteAliasResponse:
        """Deletes a created alias."""
        return self._get_stub().DeleteAlias(request)

    def delete_uut_instance(
        self, request: metadata_store_service_pb2.DeleteUutInstanceRequest
    ) -> metadata_store_service_pb2.DeleteUutInstanceResponse:
        """Deletes a UUT instance."""
        return self._get_stub().DeleteUutInstance(request)

    def batch_delete_uut_instances(
        self, request: metadata_store_service_pb2.BatchDeleteUutInstancesRequest
    ) -> metadata_store_service_pb2.BatchDeleteUutInstancesResponse:
        """Deletes multiple UUT instances atomically."""
        return self._get_stub().BatchDeleteUutInstances(request)

    def delete_uut(
        self, request: metadata_store_service_pb2.DeleteUutRequest
    ) -> metadata_store_service_pb2.DeleteUutResponse:
        """Deletes a UUT."""
        return self._get_stub().DeleteUut(request)

    def batch_delete_uuts(
        self, request: metadata_store_service_pb2.BatchDeleteUutsRequest
    ) -> metadata_store_service_pb2.BatchDeleteUutsResponse:
        """Deletes multiple UUTs atomically."""
        return self._get_stub().BatchDeleteUuts(request)

    def delete_operator(
        self, request: metadata_store_service_pb2.DeleteOperatorRequest
    ) -> metadata_store_service_pb2.DeleteOperatorResponse:
        """Deletes an operator."""
        return self._get_stub().DeleteOperator(request)

    def batch_delete_operators(
        self, request: metadata_store_service_pb2.BatchDeleteOperatorsRequest
    ) -> metadata_store_service_pb2.BatchDeleteOperatorsResponse:
        """Deletes multiple operators atomically."""
        return self._get_stub().BatchDeleteOperators(request)

    def delete_test_description(
        self, request: metadata_store_service_pb2.DeleteTestDescriptionRequest
    ) -> metadata_store_service_pb2.DeleteTestDescriptionResponse:
        """Deletes a test description."""
        return self._get_stub().DeleteTestDescription(request)

    def batch_delete_test_descriptions(
        self, request: metadata_store_service_pb2.BatchDeleteTestDescriptionsRequest
    ) -> metadata_store_service_pb2.BatchDeleteTestDescriptionsResponse:
        """Deletes multiple test descriptions atomically."""
        return self._get_stub().BatchDeleteTestDescriptions(request)

    def delete_test(
        self, request: metadata_store_service_pb2.DeleteTestRequest
    ) -> metadata_store_service_pb2.DeleteTestResponse:
        """Deletes a test."""
        return self._get_stub().DeleteTest(request)

    def batch_delete_tests(
        self, request: metadata_store_service_pb2.BatchDeleteTestsRequest
    ) -> metadata_store_service_pb2.BatchDeleteTestsResponse:
        """Deletes multiple tests atomically."""
        return self._get_stub().BatchDeleteTests(request)

    def delete_test_station(
        self, request: metadata_store_service_pb2.DeleteTestStationRequest
    ) -> metadata_store_service_pb2.DeleteTestStationResponse:
        """Deletes a test station."""
        return self._get_stub().DeleteTestStation(request)

    def batch_delete_test_stations(
        self, request: metadata_store_service_pb2.BatchDeleteTestStationsRequest
    ) -> metadata_store_service_pb2.BatchDeleteTestStationsResponse:
        """Deletes multiple test stations atomically."""
        return self._get_stub().BatchDeleteTestStations(request)

    def delete_hardware_item(
        self, request: metadata_store_service_pb2.DeleteHardwareItemRequest
    ) -> metadata_store_service_pb2.DeleteHardwareItemResponse:
        """Deletes a hardware item."""
        return self._get_stub().DeleteHardwareItem(request)

    def batch_delete_hardware_items(
        self, request: metadata_store_service_pb2.BatchDeleteHardwareItemsRequest
    ) -> metadata_store_service_pb2.BatchDeleteHardwareItemsResponse:
        """Deletes multiple hardware items atomically."""
        return self._get_stub().BatchDeleteHardwareItems(request)

    def delete_software_item(
        self, request: metadata_store_service_pb2.DeleteSoftwareItemRequest
    ) -> metadata_store_service_pb2.DeleteSoftwareItemResponse:
        """Deletes a software item."""
        return self._get_stub().DeleteSoftwareItem(request)

    def batch_delete_software_items(
        self, request: metadata_store_service_pb2.BatchDeleteSoftwareItemsRequest
    ) -> metadata_store_service_pb2.BatchDeleteSoftwareItemsResponse:
        """Deletes multiple software items atomically."""
        return self._get_stub().BatchDeleteSoftwareItems(request)

    def delete_test_adapter(
        self, request: metadata_store_service_pb2.DeleteTestAdapterRequest
    ) -> metadata_store_service_pb2.DeleteTestAdapterResponse:
        """Deletes a test adapter."""
        return self._get_stub().DeleteTestAdapter(request)

    def batch_delete_test_adapters(
        self, request: metadata_store_service_pb2.BatchDeleteTestAdaptersRequest
    ) -> metadata_store_service_pb2.BatchDeleteTestAdaptersResponse:
        """Deletes multiple test adapters atomically."""
        return self._get_stub().BatchDeleteTestAdapters(request)

    def delete_schema(
        self, request: metadata_store_service_pb2.DeleteSchemaRequest
    ) -> metadata_store_service_pb2.DeleteSchemaResponse:
        """Deletes a schema."""
        return self._get_stub().DeleteSchema(request)

    def batch_delete_schemas(
        self, request: metadata_store_service_pb2.BatchDeleteSchemasRequest
    ) -> metadata_store_service_pb2.BatchDeleteSchemasResponse:
        """Deletes multiple schemas atomically."""
        return self._get_stub().BatchDeleteSchemas(request)

    def batch_delete_aliases(
        self, request: metadata_store_service_pb2.BatchDeleteAliasesRequest
    ) -> metadata_store_service_pb2.BatchDeleteAliasesResponse:
        """Deletes multiple aliases atomically."""
        return self._get_stub().BatchDeleteAliases(request)

    def create_from_json_document(
        self, request: metadata_store_service_pb2.CreateFromJsonDocumentRequest
    ) -> metadata_store_service_pb2.CreateFromJsonDocumentResponse:
        """Creates metadata from a JSON document."""
        return self._get_stub().CreateFromJsonDocument(request)
