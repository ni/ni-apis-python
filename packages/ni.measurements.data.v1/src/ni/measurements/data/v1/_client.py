from collections.abc import Sequence
import logging

from google.protobuf import timestamp_pb2
from ni.apis.python import GrpcClient
from ni.measurementlink.discovery.v1 import DiscoveryClient, discovery_service_pb2

from . import data_store_pb2, data_store_service_pb2, data_store_service_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataStoreClient(GrpcClient):
    def __init__(self):
        super().__init__("DataStore")
        self._stub: data_store_service_pb2_grpc.DataStoreServiceStub | None = None

    async def _get_service_location(self) -> discovery_service_pb2.ServiceLocation:
        discovery_client = DiscoveryClient()
        data_store_service_name = data_store_service_pb2.DESCRIPTOR.services_by_name[
            "DataStoreService"
        ].full_name
        service_location = await discovery_client.resolve_service(
            data_store_service_name, data_store_service_name
        )
        return service_location

    @GrpcClient.log_errors
    async def create_session(self, session_metadata: data_store_pb2.SessionMetadata) -> str:
        logger.info(f"Creating session with name: {session_metadata.session_name}")

        stub = await self._get_stub()
        create_session_request = data_store_service_pb2.CreateSessionRequest(
            session_metadata=session_metadata
        )
        create_session_response = await stub.CreateSession(create_session_request)

        logger.info(f"Successfully created session with id: {create_session_response.session_id}")

        return create_session_response.session_id

    @GrpcClient.log_errors
    async def create_measurement(
        self, measurement_metadata: data_store_pb2.MeasurementMetadata
    ) -> str:
        logger.info(
            f"Creating measurement with name: {measurement_metadata.name} in session: {measurement_metadata.session_id}"
        )

        stub = await self._get_stub()
        create_measurement_request = data_store_service_pb2.CreateMeasurementRequest(
            measurement=measurement_metadata
        )
        create_measurement_response = await stub.CreateMeasurement(create_measurement_request)

        logger.info(f"Successfully created measurement with id: {create_measurement_response.id}")

        return create_measurement_response.id

    @GrpcClient.log_errors
    async def publish_condition_set_batch(
        self,
        condition_set: Sequence[data_store_pb2.ConditionArray],
        measurement_id: str,
        publish_location: data_store_pb2.PublishDataLocation.ValueType = data_store_pb2.PublishDataLocation.PUBLISH_DATA_LOCATION_LOCAL,
    ) -> data_store_pb2.StoredConditionSetValue:
        logger.info(f"Publishing condition set batch for measurement: {measurement_id}")

        stub = await self._get_stub()
        publish_condition_set_batch_request = (
            data_store_service_pb2.PublishConditionSetBatchRequest(
                condition_set=condition_set,
                publish_location=publish_location,
                measurement_id=measurement_id,
            )
        )
        publish_condition_set_batch_response = await stub.PublishConditionSetBatch(
            publish_condition_set_batch_request
        )
        logger.info(
            f"Successfully published condition set batch with id: {publish_condition_set_batch_response.stored_condition_set_value.metadata.id}"
        )

        return publish_condition_set_batch_response.stored_condition_set_value

    @GrpcClient.log_errors
    async def publish_data(
        self,
        data: data_store_pb2.PublishableData,
        timestamp: timestamp_pb2.Timestamp,
        measurement_id: str,
        notes: str = "",
        publish_location: data_store_pb2.PublishDataLocation.ValueType = data_store_pb2.PublishDataLocation.PUBLISH_DATA_LOCATION_LOCAL,
        pass_fail_status: data_store_pb2.PassFailStatus.ValueType = data_store_pb2.PassFailStatus.PASS_FAIL_STATUS_UNSPECIFIED,
        error_state: data_store_pb2.ErrorState.ValueType = data_store_pb2.ErrorState.ERROR_STATE_UNSPECIFIED,
        error_message: data_store_pb2.ErrorMessage = data_store_pb2.ErrorMessage(),
    ) -> data_store_pb2.StoredDataValue:
        logger.info(f"Publishing data with name: {data.name} for measurement: {measurement_id}")

        stub = await self._get_stub()
        publish_data_request = data_store_service_pb2.PublishDataRequest(
            data=data,
            notes=notes,
            publish_location=publish_location,
            timestamp=timestamp,
            pass_fail_status=pass_fail_status,
            error_state=error_state,
            error_message=error_message,
            measurement_id=measurement_id,
        )
        publish_data_response = await stub.PublishData(publish_data_request)
        logger.info(
            f"Successfully published data with id: {publish_data_response.stored_data_value.metadata.id}"
        )

        return publish_data_response.stored_data_value

    @GrpcClient.log_errors
    async def publish_data_batch(
        self,
        data: data_store_pb2.PublishableDataBatch,
        timestamp: Sequence[timestamp_pb2.Timestamp],
        measurement_id: str,
        publish_location: data_store_pb2.PublishDataLocation.ValueType = data_store_pb2.PublishDataLocation.PUBLISH_DATA_LOCATION_LOCAL,
        pass_fail_status: Sequence[data_store_pb2.PassFailStatus.ValueType] = [],
        error_state: Sequence[data_store_pb2.ErrorState.ValueType] = [],
        error_message: Sequence[data_store_pb2.ErrorMessage] = [],
    ) -> Sequence[data_store_pb2.StoredDataValue]:
        logger.info(
            f"Publishing data batch with name: {data.name} for measurement: {measurement_id}"
        )

        stub = await self._get_stub()
        publish_data_batch_request = data_store_service_pb2.PublishDataBatchRequest(
            data=data,
            publish_location=publish_location,
            timestamp=timestamp,
            pass_fail_status=pass_fail_status,
            error_state=error_state,
            error_message=error_message,
            measurement_id=measurement_id,
        )
        publish_data_batch_response = await stub.PublishDataBatch(publish_data_batch_request)
        logger.info(
            f"Successfully published data batch with {len(publish_data_batch_response.stored_data_values)} items"
        )

        return publish_data_batch_response.stored_data_values

    async def query_data(self, odata_query: str) -> Sequence[data_store_pb2.StoredDataValue]:
        logger.info(f"Querying data with OData query: {odata_query}")

        stub = await self._get_stub()
        query_data_request = data_store_service_pb2.QueryDataRequest(odata_query=odata_query)
        query_data_response = await stub.QueryData(query_data_request)

        logger.info(
            f"Successfully queried data and received {len(query_data_response.stored_data_values)} items"
        )

        return query_data_response.stored_data_values

    async def _get_stub(self) -> data_store_service_pb2_grpc.DataStoreServiceStub:
        if self._stub is None:
            channel = await self._get_or_create_channel()
            self._stub = data_store_service_pb2_grpc.DataStoreServiceStub(channel)

        return self._stub
