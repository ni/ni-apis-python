import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import grpc
import ni.measurements.data.v2.data_store_pb2 as data_store_types
import ni.measurements.data.v2.data_store_service_pb2 as service_types
import pytest
from google.protobuf import empty_pb2
from google.protobuf.message import Message
from pytest_mock import MockerFixture

from ni.measurements.data.v2.client import DataStoreClient

RPC_CASES: list[tuple[str, str, type[Message], type[Message]]] = [
    (
        "CreateTestResult",
        "create_test_result",
        service_types.CreateTestResultRequest,
        data_store_types.TestResult,
    ),
    (
        "BatchCreateTestResults",
        "batch_create_test_results",
        service_types.BatchCreateTestResultsRequest,
        service_types.BatchCreateTestResultsResponse,
    ),
    (
        "GetTestResult",
        "get_test_result",
        service_types.GetTestResultRequest,
        data_store_types.TestResult,
    ),
    (
        "QueryTestResults",
        "query_test_results",
        service_types.QueryTestResultsRequest,
        service_types.QueryTestResultsResponse,
    ),
    (
        "UpdateTestResult",
        "update_test_result",
        service_types.UpdateTestResultRequest,
        data_store_types.TestResult,
    ),
    (
        "BatchUpdateTestResults",
        "batch_update_test_results",
        service_types.BatchUpdateTestResultsRequest,
        service_types.BatchUpdateTestResultsResponse,
    ),
    (
        "AddTestResultMetadata",
        "add_test_result_metadata",
        service_types.AddTestResultMetadataRequest,
        service_types.AddTestResultMetadataResponse,
    ),
    (
        "RemoveTestResultMetadata",
        "remove_test_result_metadata",
        service_types.RemoveTestResultMetadataRequest,
        service_types.RemoveTestResultMetadataResponse,
    ),
    (
        "DeleteTestResult",
        "delete_test_result",
        service_types.DeleteTestResultRequest,
        empty_pb2.Empty,
    ),
    (
        "BatchDeleteTestResults",
        "batch_delete_test_results",
        service_types.BatchDeleteTestResultsRequest,
        service_types.BatchDeleteTestResultsResponse,
    ),
    ("CreateStep", "create_step", service_types.CreateStepRequest, data_store_types.Step),
    (
        "BatchCreateSteps",
        "batch_create_steps",
        service_types.BatchCreateStepsRequest,
        service_types.BatchCreateStepsResponse,
    ),
    ("GetStep", "get_step", service_types.GetStepRequest, data_store_types.Step),
    (
        "QuerySteps",
        "query_steps",
        service_types.QueryStepsRequest,
        service_types.QueryStepsResponse,
    ),
    ("UpdateStep", "update_step", service_types.UpdateStepRequest, data_store_types.Step),
    (
        "BatchUpdateSteps",
        "batch_update_steps",
        service_types.BatchUpdateStepsRequest,
        service_types.BatchUpdateStepsResponse,
    ),
    (
        "AddCondition",
        "add_condition",
        service_types.AddConditionRequest,
        service_types.AddConditionResponse,
    ),
    (
        "RemoveCondition",
        "remove_condition",
        service_types.RemoveConditionRequest,
        service_types.RemoveConditionResponse,
    ),
    ("DeleteStep", "delete_step", service_types.DeleteStepRequest, empty_pb2.Empty),
    (
        "BatchDeleteSteps",
        "batch_delete_steps",
        service_types.BatchDeleteStepsRequest,
        service_types.BatchDeleteStepsResponse,
    ),
    (
        "CreateMeasurement",
        "create_measurement",
        service_types.CreateMeasurementRequest,
        data_store_types.Measurement,
    ),
    (
        "BatchCreateMeasurements",
        "batch_create_measurements",
        service_types.BatchCreateMeasurementsRequest,
        service_types.BatchCreateMeasurementsResponse,
    ),
    (
        "GetMeasurement",
        "get_measurement",
        service_types.GetMeasurementRequest,
        data_store_types.Measurement,
    ),
    (
        "QueryMeasurements",
        "query_measurements",
        service_types.QueryMeasurementsRequest,
        service_types.QueryMeasurementsResponse,
    ),
    (
        "UpdateMeasurement",
        "update_measurement",
        service_types.UpdateMeasurementRequest,
        data_store_types.Measurement,
    ),
    (
        "BatchUpdateMeasurements",
        "batch_update_measurements",
        service_types.BatchUpdateMeasurementsRequest,
        service_types.BatchUpdateMeasurementsResponse,
    ),
    (
        "AddMeasurementMetadata",
        "add_measurement_metadata",
        service_types.AddMeasurementMetadataRequest,
        service_types.AddMeasurementMetadataResponse,
    ),
    (
        "RemoveMeasurementMetadata",
        "remove_measurement_metadata",
        service_types.RemoveMeasurementMetadataRequest,
        service_types.RemoveMeasurementMetadataResponse,
    ),
    (
        "DeleteMeasurement",
        "delete_measurement",
        service_types.DeleteMeasurementRequest,
        empty_pb2.Empty,
    ),
    (
        "BatchDeleteMeasurements",
        "batch_delete_measurements",
        service_types.BatchDeleteMeasurementsRequest,
        service_types.BatchDeleteMeasurementsResponse,
    ),
    (
        "ReadMeasurementValues",
        "read_measurement_values",
        service_types.ReadMeasurementValuesRequest,
        service_types.ReadMeasurementValuesResponse,
    ),
]


def test_rpc_cases_cover_every_service_method() -> None:
    service = service_types.DESCRIPTOR.services_by_name["DataStoreService"]

    assert Counter(case[0] for case in RPC_CASES) == Counter(
        method.name for method in service.methods
    )

    for rpc_name, client_method, request_type, response_type in RPC_CASES:
        method = service.methods_by_name[rpc_name]
        assert client_method == re.sub(r"(?<!^)(?=[A-Z])", "_", rpc_name).lower()
        assert callable(getattr(DataStoreClient, client_method, None)), client_method
        assert request_type.DESCRIPTOR == method.input_type, rpc_name
        assert response_type.DESCRIPTOR == method.output_type, rpc_name


@pytest.mark.parametrize("rpc_name,client_method,request_type,response_type", RPC_CASES)
def test_rpc_methods_pass_request_and_response_through(
    mocker: MockerFixture,
    rpc_name: str,
    client_method: str,
    request_type: type[Message],
    response_type: type[Message],
) -> None:
    stub = Mock()
    request = request_type()
    response = response_type()
    getattr(stub, rpc_name).return_value = response
    mocker.patch.object(DataStoreClient, "_get_stub", return_value=stub)
    client = DataStoreClient()

    actual = getattr(client, client_method)(request)

    getattr(stub, rpc_name).assert_called_once_with(request)
    assert getattr(stub, rpc_name).call_args.args[0] is request
    assert actual is response


@pytest.mark.parametrize("rpc_name,client_method,request_type", [case[:3] for case in RPC_CASES])
def test_rpc_errors_propagate_unchanged(
    mocker: MockerFixture,
    rpc_name: str,
    client_method: str,
    request_type: type[Message],
) -> None:
    error = grpc.RpcError("request failed")
    stub = Mock()
    request = request_type()
    getattr(stub, rpc_name).side_effect = error
    mocker.patch.object(DataStoreClient, "_get_stub", return_value=stub)
    client = DataStoreClient()

    with pytest.raises(grpc.RpcError) as raised:
        getattr(client, client_method)(request)

    assert raised.value is error
    getattr(stub, rpc_name).assert_called_once_with(request)


def test_cancelled_rpc_error_propagates_unchanged(mocker: MockerFixture) -> None:
    class CancelledRpcError(grpc.RpcError):
        def code(self) -> grpc.StatusCode:
            return grpc.StatusCode.CANCELLED

    error = CancelledRpcError()
    stub = Mock()
    stub.GetMeasurement.side_effect = error
    mocker.patch.object(DataStoreClient, "_get_stub", return_value=stub)
    client = DataStoreClient()

    with pytest.raises(grpc.RpcError) as raised:
        client.get_measurement(service_types.GetMeasurementRequest())

    assert raised.value is error
    assert raised.value.code() == grpc.StatusCode.CANCELLED


def test_injected_channel_is_used_without_discovery(mocker: MockerFixture) -> None:
    channel = Mock(spec=grpc.Channel)
    stub_class = mocker.patch("ni.measurements.data.v2.client._client.DataStoreServiceStub")

    client = DataStoreClient(grpc_channel=channel)

    stub_class.assert_called_once_with(channel)
    client.close()
    channel.close.assert_not_called()


def test_client_lazily_discovers_service_and_closes_owned_pool(mocker: MockerFixture) -> None:
    pool_class = mocker.patch("ni.measurements.data.v2.client._client_base.GrpcChannelPool")
    discovery_class = mocker.patch("ni.measurements.data.v2.client._client_base.DiscoveryClient")
    stub_class = mocker.patch("ni.measurements.data.v2.client._client.DataStoreServiceStub")
    discovery = discovery_class.return_value
    discovery.enumerate_compute_nodes.return_value = []
    discovery.resolve_service.return_value.insecure_address = "localhost:50051"
    pool = pool_class.return_value
    channel = pool.get_channel.return_value
    client = DataStoreClient()

    stub = client._get_stub()

    pool_class.assert_called_once_with()
    discovery_class.assert_called_once_with(grpc_channel_pool=pool)
    discovery.resolve_service.assert_called_once_with(
        provided_interface="ni.measurements.data.v2.DataStoreService",
        deployment_target="",
        service_class="",
    )
    pool.get_channel.assert_called_once_with("localhost:50051")
    stub_class.assert_called_once_with(channel)
    assert stub is stub_class.return_value

    client.close()

    pool.close.assert_called_once_with()


def test_client_does_not_close_caller_owned_channel_pool(mocker: MockerFixture) -> None:
    pool = Mock()
    discovery = Mock()
    discovery.enumerate_compute_nodes.return_value = []
    discovery.resolve_service.return_value.insecure_address = "localhost:50051"
    mocker.patch("ni.measurements.data.v2.client._client.DataStoreServiceStub")
    client = DataStoreClient(discovery_client=discovery, grpc_channel_pool=pool)

    client._get_stub()
    client.close()

    pool.close.assert_not_called()


def test_context_manager_closes_client_owned_pool(mocker: MockerFixture) -> None:
    pool_class = mocker.patch("ni.measurements.data.v2.client._client_base.GrpcChannelPool")
    discovery_class = mocker.patch("ni.measurements.data.v2.client._client_base.DiscoveryClient")
    discovery_class.return_value.enumerate_compute_nodes.return_value = []
    discovery_class.return_value.resolve_service.return_value.insecure_address = "localhost:50051"
    mocker.patch("ni.measurements.data.v2.client._client.DataStoreServiceStub")

    with DataStoreClient() as client:
        client._get_stub()

    pool_class.return_value.close.assert_called_once_with()


def test_client_reuse_after_close_creates_new_resources(mocker: MockerFixture) -> None:
    pool_class = mocker.patch("ni.measurements.data.v2.client._client_base.GrpcChannelPool")
    discovery_class = mocker.patch("ni.measurements.data.v2.client._client_base.DiscoveryClient")
    discovery_class.return_value.enumerate_compute_nodes.return_value = []
    discovery_class.return_value.resolve_service.return_value.insecure_address = "localhost:50051"
    stub_class = mocker.patch("ni.measurements.data.v2.client._client.DataStoreServiceStub")
    first_stub, second_stub = Mock(), Mock()
    stub_class.side_effect = [first_stub, second_stub]
    client = DataStoreClient()

    actual_first_stub = client._get_stub()
    client.close()
    actual_second_stub = client._get_stub()

    assert actual_first_stub is first_stub
    assert actual_second_stub is second_stub
    assert pool_class.call_count == 2
    assert discovery_class.call_count == 2
    pool_class.return_value.close.assert_called_once_with()
    client.close()


def test_close_during_stub_initialization_does_not_return_none(mocker: MockerFixture) -> None:
    class CloseAfterLockRelease:
        def __init__(self) -> None:
            self.client: DataStoreClient | None = None
            self.close_on_release = False

        def __enter__(self) -> "CloseAfterLockRelease":
            return self

        def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
            if self.close_on_release:
                self.close_on_release = False
                assert self.client is not None
                self.client.close()

    discovery = Mock()
    discovery.enumerate_compute_nodes.return_value = []
    discovery.resolve_service.return_value.insecure_address = "localhost:50051"
    pool = Mock()
    stub_class = mocker.patch("ni.measurements.data.v2.client._client.DataStoreServiceStub")
    client = DataStoreClient(discovery_client=discovery, grpc_channel_pool=pool)
    lock = CloseAfterLockRelease()
    lock.client = client
    lock.close_on_release = True
    client._lock = lock  # type: ignore[assignment]

    stub = client._get_stub()

    assert stub is stub_class.return_value


def test_client_calls_v2_service_over_injected_channel() -> None:
    server = grpc.server(ThreadPoolExecutor(max_workers=1))
    handler = grpc.unary_unary_rpc_method_handler(
        lambda request, context: data_store_types.Measurement(),
        request_deserializer=service_types.GetMeasurementRequest.FromString,
        response_serializer=data_store_types.Measurement.SerializeToString,
    )
    service_handler = grpc.method_handlers_generic_handler(
        "ni.measurements.data.v2.DataStoreService",
        {"GetMeasurement": handler},
    )
    server.add_generic_rpc_handlers((service_handler,))
    port = server.add_insecure_port("localhost:0")
    server.start()
    channel = grpc.insecure_channel(f"localhost:{port}")
    client = DataStoreClient(grpc_channel=channel)
    try:
        result = client.get_measurement(service_types.GetMeasurementRequest())

        assert isinstance(result, data_store_types.Measurement)
    finally:
        client.close()
        channel.close()
        server.stop(0).wait()


def test_read_measurement_values_transports_mask_and_optional_limits() -> None:
    request = service_types.ReadMeasurementValuesRequest(measurement_id="measurement-id")
    request.read_mask.paths.extend(["value", "upper_limit"])
    response = service_types.ReadMeasurementValuesResponse()
    response.value.json_value.value.update({"samples": [1, 2]})
    response.upper_limit.json_value.value.update({"maximum": 3})
    received_requests: list[service_types.ReadMeasurementValuesRequest] = []

    def read_values(
        received: service_types.ReadMeasurementValuesRequest, context: grpc.ServicerContext
    ) -> service_types.ReadMeasurementValuesResponse:
        received_requests.append(received)
        return response

    with ThreadPoolExecutor(max_workers=1) as executor:
        server = grpc.server(executor)
        handler = grpc.unary_unary_rpc_method_handler(
            read_values,
            request_deserializer=service_types.ReadMeasurementValuesRequest.FromString,
            response_serializer=service_types.ReadMeasurementValuesResponse.SerializeToString,
        )
        server.add_generic_rpc_handlers(
            (
                grpc.method_handlers_generic_handler(
                    "ni.measurements.data.v2.DataStoreService", {"ReadMeasurementValues": handler}
                ),
            )
        )
        port = server.add_insecure_port("127.0.0.1:0")
        assert port != 0
        server.start()
        try:
            with grpc.insecure_channel(f"127.0.0.1:{port}") as channel:
                grpc.channel_ready_future(channel).result(timeout=5)
                with DataStoreClient(grpc_channel=channel) as client:
                    result = client.read_measurement_values(request)

                assert received_requests == [request]
                assert result == response
                assert result.HasField("value")
                assert result.HasField("upper_limit")
                assert not result.HasField("lower_limit")
        finally:
            server.stop(0).wait()
