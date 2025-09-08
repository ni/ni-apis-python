"""Client for accessing the NI Data Store Service."""

from typing import Optional

import grpc
import ni.measurements.data.v1.data_store_service_pb2 as data_store_service_pb2
import ni.measurements.data.v1.data_store_service_pb2_grpc as data_store_service_pb2_grpc
from ni.measurementlink.discovery.v1.client import DiscoveryClient
from ni_grpc_extensions.channelpool import GrpcChannelPool

from ni.measurements.data.v1.client._client_base import GrpcServiceClientBase

GRPC_SERVICE_INTERFACE_NAME = "ni.measurements.data.v1.DataStoreService"


class DataStoreClient(GrpcServiceClientBase):
    """Client for accessing the NI Data Store Service."""

    def __init__(
        self,
        *,
        discovery_client: Optional[DiscoveryClient] = None,
        grpc_channel: Optional[grpc.Channel] = None,
        grpc_channel_pool: Optional[GrpcChannelPool] = None,
    ) -> None:
        """Initialize the Data Store Client.

        Args:
            discovery_client: An optional discovery client (recommended).

            grpc_channel: An optional data store gRPC channel.

            grpc_channel_pool: An optional gRPC channel pool (recommended).
        """
        super().__init__(
            discovery_client=discovery_client,
            grpc_channel=grpc_channel,
            grpc_channel_pool=grpc_channel_pool,
            service_interface_name=GRPC_SERVICE_INTERFACE_NAME,
            service_class="",
            stub_class=data_store_service_pb2_grpc.DataStoreServiceStub,
        )

    def create_session(
        self, request: data_store_service_pb2.CreateSessionRequest
    ) -> data_store_service_pb2.CreateSessionResponse:
        """Creates a new session in the data store."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.CreateSession(request)

    def get_session(
        self, request: data_store_service_pb2.GetSessionRequest
    ) -> data_store_service_pb2.GetSessionResponse:
        """Gets the session associated with the identifier given in the request."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.GetSession(request)

    def create_measurement(
        self, request: data_store_service_pb2.CreateMeasurementRequest
    ) -> data_store_service_pb2.CreateMeasurementResponse:
        """Creates a new measurement in the data store."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.CreateMeasurement(request)

    def get_measurement(
        self, request: data_store_service_pb2.GetMeasurementRequest
    ) -> data_store_service_pb2.GetMeasurementResponse:
        """Gets the measurement associated with the identifier given in the request."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.GetMeasurement(request)

    def query_measurements(
        self, request: data_store_service_pb2.QueryMeasurementsRequest
    ) -> data_store_service_pb2.QueryMeasurementsResponse:
        """Query for measurements matching the given OData query."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.QueryMeasurements(request)

    def publish_condition_set(
        self, request: data_store_service_pb2.PublishConditionSetRequest
    ) -> data_store_service_pb2.PublishConditionSetResponse:
        """Publishes a single condition set for a measurement."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.PublishConditionSet(request)

    def publish_condition(
        self, request: data_store_service_pb2.PublishConditionRequest
    ) -> data_store_service_pb2.PublishConditionResponse:
        """Publishes a single condition value for a measurement."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.PublishCondition(request)

    def publish_condition_set_batch(
        self, request: data_store_service_pb2.PublishConditionSetBatchRequest
    ) -> data_store_service_pb2.PublishConditionSetBatchResponse:
        """Publishes the complete set of conditions for a measurement."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.PublishConditionSetBatch(request)

    def publish_condition_batch(
        self, request: data_store_service_pb2.PublishConditionBatchRequest
    ) -> data_store_service_pb2.PublishConditionBatchResponse:
        """Publishes a batch of condition values for a measurement."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.PublishConditionBatch(request)

    def publish_data(
        self, request: data_store_service_pb2.PublishDataRequest
    ) -> data_store_service_pb2.PublishDataResponse:
        """Publishes a single data value."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.PublishData(request)

    def publish_data_batch(
        self, request: data_store_service_pb2.PublishDataBatchRequest
    ) -> data_store_service_pb2.PublishDataBatchResponse:
        """Publishes a batch of scalar data values."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.PublishDataBatch(request)

    def query_condition_sets(
        self, request: data_store_service_pb2.QueryConditionSetsRequest
    ) -> data_store_service_pb2.QueryConditionSetsResponse:
        """Queries the condition sets in the data store, based on an OData query."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.QueryConditionSets(request)

    def query_conditions(
        self, request: data_store_service_pb2.QueryConditionsRequest
    ) -> data_store_service_pb2.QueryConditionsResponse:
        """Queries the conditions in the data store, based on an OData query."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.QueryConditions(request)

    def query_data(
        self, request: data_store_service_pb2.QueryDataRequest
    ) -> data_store_service_pb2.QueryDataResponse:
        """Queries the data in the data store, based on an OData query."""
        stub: data_store_service_pb2_grpc.DataStoreServiceStub = self._get_stub()
        return stub.QueryData(request)
