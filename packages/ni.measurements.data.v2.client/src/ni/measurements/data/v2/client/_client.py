"""Client for accessing the NI Data Store Service."""

from __future__ import annotations

import grpc
from google.protobuf import empty_pb2
from ni.measurementlink.discovery.v1.client import DiscoveryClient
from ni.measurements.data.v2 import data_store_pb2, data_store_service_pb2
from ni.measurements.data.v2.data_store_service_pb2_grpc import DataStoreServiceStub
from ni_grpc_extensions.channelpool import GrpcChannelPool

from ni.measurements.data.v2.client._client_base import GrpcServiceClientBase


class DataStoreClient(GrpcServiceClientBase[DataStoreServiceStub]):
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
            service_interface_name="ni.measurements.data.v2.DataStoreService",
            service_class="",
            stub_class=DataStoreServiceStub,
        )

    def create_test_result(
        self, request: data_store_service_pb2.CreateTestResultRequest
    ) -> data_store_pb2.TestResult:
        """Create a test result object for publishing measurements."""
        return self._get_stub().CreateTestResult(request)

    def batch_create_test_results(
        self, request: data_store_service_pb2.BatchCreateTestResultsRequest
    ) -> data_store_service_pb2.BatchCreateTestResultsResponse:
        """Create multiple test results at once."""
        return self._get_stub().BatchCreateTestResults(request)

    def get_test_result(
        self, request: data_store_service_pb2.GetTestResultRequest
    ) -> data_store_pb2.TestResult:
        """Get the test result associated with the identifier given in the request."""
        return self._get_stub().GetTestResult(request)

    def query_test_results(
        self, request: data_store_service_pb2.QueryTestResultsRequest
    ) -> data_store_service_pb2.QueryTestResultsResponse:
        """Query for test results matching the given OData query."""
        return self._get_stub().QueryTestResults(request)

    def update_test_result(
        self, request: data_store_service_pb2.UpdateTestResultRequest
    ) -> data_store_pb2.TestResult:
        """Update the test result associated with the identifier given in the request."""
        return self._get_stub().UpdateTestResult(request)

    def batch_update_test_results(
        self, request: data_store_service_pb2.BatchUpdateTestResultsRequest
    ) -> data_store_service_pb2.BatchUpdateTestResultsResponse:
        """Update multiple test results at once."""
        return self._get_stub().BatchUpdateTestResults(request)

    def add_test_result_metadata(
        self, request: data_store_service_pb2.AddTestResultMetadataRequest
    ) -> data_store_service_pb2.AddTestResultMetadataResponse:
        """Add metadata to the test result identified by the request."""
        return self._get_stub().AddTestResultMetadata(request)

    def remove_test_result_metadata(
        self, request: data_store_service_pb2.RemoveTestResultMetadataRequest
    ) -> data_store_service_pb2.RemoveTestResultMetadataResponse:
        """Remove metadata from the test result identified by the request."""
        return self._get_stub().RemoveTestResultMetadata(request)

    def delete_test_result(
        self, request: data_store_service_pb2.DeleteTestResultRequest
    ) -> empty_pb2.Empty:
        """Delete the test result associated with the identifier given in the request."""
        return self._get_stub().DeleteTestResult(request)

    def batch_delete_test_results(
        self, request: data_store_service_pb2.BatchDeleteTestResultsRequest
    ) -> data_store_service_pb2.BatchDeleteTestResultsResponse:
        """Delete multiple test results at once."""
        return self._get_stub().BatchDeleteTestResults(request)

    def create_step(self, request: data_store_service_pb2.CreateStepRequest) -> data_store_pb2.Step:
        """Create a new step in the data store."""
        return self._get_stub().CreateStep(request)

    def batch_create_steps(
        self, request: data_store_service_pb2.BatchCreateStepsRequest
    ) -> data_store_service_pb2.BatchCreateStepsResponse:
        """Create multiple steps at once."""
        return self._get_stub().BatchCreateSteps(request)

    def get_step(self, request: data_store_service_pb2.GetStepRequest) -> data_store_pb2.Step:
        """Get the step associated with the identifier given in the request."""
        return self._get_stub().GetStep(request)

    def query_steps(
        self, request: data_store_service_pb2.QueryStepsRequest
    ) -> data_store_service_pb2.QueryStepsResponse:
        """Query for steps matching the given OData query."""
        return self._get_stub().QuerySteps(request)

    def update_step(self, request: data_store_service_pb2.UpdateStepRequest) -> data_store_pb2.Step:
        """Update the step associated with the identifier given in the request."""
        return self._get_stub().UpdateStep(request)

    def batch_update_steps(
        self, request: data_store_service_pb2.BatchUpdateStepsRequest
    ) -> data_store_service_pb2.BatchUpdateStepsResponse:
        """Update multiple steps at once."""
        return self._get_stub().BatchUpdateSteps(request)

    def add_condition(
        self, request: data_store_service_pb2.AddConditionRequest
    ) -> data_store_service_pb2.AddConditionResponse:
        """Add a condition to the step associated with the identifier given in the request."""
        return self._get_stub().AddCondition(request)

    def remove_condition(
        self, request: data_store_service_pb2.RemoveConditionRequest
    ) -> data_store_service_pb2.RemoveConditionResponse:
        """Remove a condition from the step associated with the identifier given in the request."""
        return self._get_stub().RemoveCondition(request)

    def delete_step(self, request: data_store_service_pb2.DeleteStepRequest) -> empty_pb2.Empty:
        """Delete the step associated with the identifier given in the request."""
        return self._get_stub().DeleteStep(request)

    def batch_delete_steps(
        self, request: data_store_service_pb2.BatchDeleteStepsRequest
    ) -> data_store_service_pb2.BatchDeleteStepsResponse:
        """Delete multiple steps at once."""
        return self._get_stub().BatchDeleteSteps(request)

    def create_measurement(
        self, request: data_store_service_pb2.CreateMeasurementRequest
    ) -> data_store_pb2.Measurement:
        """Create a new measurement in the data store."""
        return self._get_stub().CreateMeasurement(request)

    def batch_create_measurements(
        self, request: data_store_service_pb2.BatchCreateMeasurementsRequest
    ) -> data_store_service_pb2.BatchCreateMeasurementsResponse:
        """Create multiple measurements at once."""
        return self._get_stub().BatchCreateMeasurements(request)

    def get_measurement(
        self, request: data_store_service_pb2.GetMeasurementRequest
    ) -> data_store_pb2.Measurement:
        """Get the measurement associated with the identifier given in the request."""
        return self._get_stub().GetMeasurement(request)

    def query_measurements(
        self, request: data_store_service_pb2.QueryMeasurementsRequest
    ) -> data_store_service_pb2.QueryMeasurementsResponse:
        """Query measurements using OData query syntax."""
        return self._get_stub().QueryMeasurements(request)

    def update_measurement(
        self, request: data_store_service_pb2.UpdateMeasurementRequest
    ) -> data_store_pb2.Measurement:
        """Update the measurement associated with the identifier given in the request."""
        return self._get_stub().UpdateMeasurement(request)

    def batch_update_measurements(
        self, request: data_store_service_pb2.BatchUpdateMeasurementsRequest
    ) -> data_store_service_pb2.BatchUpdateMeasurementsResponse:
        """Update multiple measurements at once."""
        return self._get_stub().BatchUpdateMeasurements(request)

    def add_measurement_metadata(
        self, request: data_store_service_pb2.AddMeasurementMetadataRequest
    ) -> data_store_service_pb2.AddMeasurementMetadataResponse:
        """Add metadata to the measurement identified by the request."""
        return self._get_stub().AddMeasurementMetadata(request)

    def remove_measurement_metadata(
        self, request: data_store_service_pb2.RemoveMeasurementMetadataRequest
    ) -> data_store_service_pb2.RemoveMeasurementMetadataResponse:
        """Remove metadata from the measurement identified by the request."""
        return self._get_stub().RemoveMeasurementMetadata(request)

    def delete_measurement(
        self, request: data_store_service_pb2.DeleteMeasurementRequest
    ) -> empty_pb2.Empty:
        """Delete the measurement associated with the identifier given in the request."""
        return self._get_stub().DeleteMeasurement(request)

    def batch_delete_measurements(
        self, request: data_store_service_pb2.BatchDeleteMeasurementsRequest
    ) -> data_store_service_pb2.BatchDeleteMeasurementsResponse:
        """Delete multiple measurements at once."""
        return self._get_stub().BatchDeleteMeasurements(request)

    def read_measurement_values(
        self, request: data_store_service_pb2.ReadMeasurementValuesRequest
    ) -> data_store_service_pb2.ReadMeasurementValuesResponse:
        """Read the value and limits of a measurement selected by the read mask."""
        return self._get_stub().ReadMeasurementValues(request)
