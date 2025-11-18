"""Client for accessing the NI Data Store Service."""

from __future__ import annotations

import grpc
import ni.measurements.data.v1.data_store_service_pb2 as data_store_service_pb2
import ni.measurements.data.v1.data_store_service_pb2_grpc as data_store_service_pb2_grpc
from ni.measurementlink.discovery.v1.client import DiscoveryClient
from ni_grpc_extensions.channelpool import GrpcChannelPool

from ni.measurements.data.v1.client._client_base import GrpcServiceClientBase


class DataStoreClient(GrpcServiceClientBase[data_store_service_pb2_grpc.DataStoreServiceStub]):
    """Client for accessing the NI Data Store Service."""

    __slots__ = ()

    def __init__(
        self,
        *,
        discovery_client: DiscoveryClient | None = None,
        grpc_channel: grpc.Channel | None = None,
        grpc_channel_pool: GrpcChannelPool | None = None,
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
            service_interface_name="ni.measurements.data.v1.DataStoreService",
            service_class="",
            stub_class=data_store_service_pb2_grpc.DataStoreServiceStub,
        )

    def create_test_result(
        self, request: data_store_service_pb2.CreateTestResultRequest
    ) -> data_store_service_pb2.CreateTestResultResponse:
        """Create a test result object for publishing measurements."""
        return self._get_stub().CreateTestResult(request)

    def get_test_result(
        self, request: data_store_service_pb2.GetTestResultRequest
    ) -> data_store_service_pb2.GetTestResultResponse:
        """Get the test result associated with the identifier given in the request."""
        return self._get_stub().GetTestResult(request)

    def query_test_results(
        self, request: data_store_service_pb2.QueryTestResultsRequest
    ) -> data_store_service_pb2.QueryTestResultsResponse:
        """Query for test results matching the given OData query."""
        return self._get_stub().QueryTestResults(request)

    def create_step(
        self, request: data_store_service_pb2.CreateStepRequest
    ) -> data_store_service_pb2.CreateStepResponse:
        """Create a new step in the data store."""
        return self._get_stub().CreateStep(request)

    def get_step(
        self, request: data_store_service_pb2.GetStepRequest
    ) -> data_store_service_pb2.GetStepResponse:
        """Get the step associated with the identifier given in the request."""
        return self._get_stub().GetStep(request)

    def query_steps(
        self, request: data_store_service_pb2.QueryStepsRequest
    ) -> data_store_service_pb2.QueryStepsResponse:
        """Query for steps matching the given OData query."""
        return self._get_stub().QuerySteps(request)

    def publish_condition(
        self, request: data_store_service_pb2.PublishConditionRequest
    ) -> data_store_service_pb2.PublishConditionResponse:
        """Publish a single condition value for a step."""
        return self._get_stub().PublishCondition(request)

    def publish_condition_batch(
        self, request: data_store_service_pb2.PublishConditionBatchRequest
    ) -> data_store_service_pb2.PublishConditionBatchResponse:
        """Publish multiple condition values at once for parametric sweeps."""
        return self._get_stub().PublishConditionBatch(request)

    def publish_measurement(
        self, request: data_store_service_pb2.PublishMeasurementRequest
    ) -> data_store_service_pb2.PublishMeasurementResponse:
        """Publish a single measurement value associated with a step."""
        return self._get_stub().PublishMeasurement(request)

    def publish_measurement_batch(
        self, request: data_store_service_pb2.PublishMeasurementBatchRequest
    ) -> data_store_service_pb2.PublishMeasurementBatchResponse:
        """Publish multiple scalar measurements at once for parametric sweeps."""
        return self._get_stub().PublishMeasurementBatch(request)

    def get_measurement(
        self, request: data_store_service_pb2.GetMeasurementRequest
    ) -> data_store_service_pb2.GetMeasurementResponse:
        """Get the measurement associated with the identifier given in the request."""
        return self._get_stub().GetMeasurement(request)

    def get_condition(
        self, request: data_store_service_pb2.GetConditionRequest
    ) -> data_store_service_pb2.GetConditionResponse:
        """Get the condition associated with the identifier given in the request."""
        return self._get_stub().GetCondition(request)

    def query_conditions(
        self, request: data_store_service_pb2.QueryConditionsRequest
    ) -> data_store_service_pb2.QueryConditionsResponse:
        """Query conditions using OData query syntax."""
        return self._get_stub().QueryConditions(request)

    def query_measurements(
        self, request: data_store_service_pb2.QueryMeasurementsRequest
    ) -> data_store_service_pb2.QueryMeasurementsResponse:
        """Query measurements using OData query syntax."""
        return self._get_stub().QueryMeasurements(request)
