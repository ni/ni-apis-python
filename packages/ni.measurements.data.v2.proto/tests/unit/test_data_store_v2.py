"""Contract tests for the generated data store V2 package."""

from concurrent.futures import ThreadPoolExecutor

import grpc
import pytest
from google.protobuf import field_mask_pb2
from ni.measurements.data.v1 import data_store_pb2 as v1
from ni.measurements.data.v2 import data_store_pb2 as v2
from ni.measurements.data.v2 import data_store_service_pb2 as service
from ni.measurements.data.v2 import data_store_service_pb2_grpc as service_grpc
from ni.protobuf.types import precision_duration_pb2


def test___nested_create_request___serialized___preserves_v2_values() -> None:
    measurement = v2.Measurement(
        name="voltage",
        duration=precision_duration_pb2.PrecisionDuration(seconds=2),
        comparison_type="GE",
    )
    measurement.value.json_value.value.update({"samples": [1, True, None]})
    request = service.CreateTestResultRequest(
        test_result=v2.TestResult(
            name="run",
            status=v2.STATUS_RUNNING,
            steps=[v2.Step(name="step", measurements=[measurement])],
        )
    )
    request.test_result.extension.update({"nested": {"enabled": True}})

    restored = service.CreateTestResultRequest.FromString(request.SerializeToString())

    assert restored == request
    assert restored.test_result.steps[0].measurements[0].value.WhichOneof("value") == ("json_value")
    assert (
        restored.test_result.extension.fields["nested"].struct_value.fields["enabled"].bool_value
        is True
    )


def test___update_request___serialized___preserves_explicit_clear_mask() -> None:
    request = service.UpdateMeasurementRequest(
        measurement=v2.Measurement(id="measurement-id", notes=""),
        update_mask=field_mask_pb2.FieldMask(paths=["notes"]),
    )

    restored = service.UpdateMeasurementRequest.FromString(request.SerializeToString())

    assert restored.update_mask.paths == ["notes"]
    assert restored.measurement.notes == ""


def test___v1_and_v2___same_process___distinct_descriptors() -> None:
    old = v1.TestResult(name="v1")
    new = v2.TestResult(name="v2", status=v2.STATUS_RUNNING)

    assert old.DESCRIPTOR.full_name == "ni.measurements.data.v1.TestResult"
    assert new.DESCRIPTOR.full_name == "ni.measurements.data.v2.TestResult"
    assert v1.TestResult.FromString(old.SerializeToString()).name == "v1"
    assert v2.TestResult.FromString(new.SerializeToString()).status == v2.STATUS_RUNNING


def _get_test_result(
    request: service.GetTestResultRequest, context: grpc.ServicerContext
) -> v2.TestResult:
    return v2.TestResult(id=request.test_result_id, name="retrieved")


def test___generated_stub___local_rpc___uses_v2_service_and_serializers() -> None:
    with ThreadPoolExecutor(max_workers=1) as executor:
        server = grpc.server(executor)
        handler = grpc.method_handlers_generic_handler(
            "ni.measurements.data.v2.DataStoreService",
            {
                "GetTestResult": grpc.unary_unary_rpc_method_handler(
                    _get_test_result,
                    request_deserializer=service.GetTestResultRequest.FromString,
                    response_serializer=v2.TestResult.SerializeToString,
                )
            },
        )
        server.add_generic_rpc_handlers((handler,))
        port = server.add_insecure_port("127.0.0.1:0")
        assert port != 0
        server.start()
        try:
            with grpc.insecure_channel(f"127.0.0.1:{port}") as channel:
                stub = service_grpc.DataStoreServiceStub(channel)
                response = stub.GetTestResult(
                    service.GetTestResultRequest(test_result_id="test-id"), timeout=5
                )
                assert response.id == "test-id"
                assert response.name == "retrieved"
                for method in service.DESCRIPTOR.services_by_name["DataStoreService"].methods:
                    assert callable(getattr(stub, method.name))

                v1_call = channel.unary_unary(
                    "/ni.measurements.data.v1.DataStoreService/GetTestResult",
                    request_serializer=service.GetTestResultRequest.SerializeToString,
                    response_deserializer=v2.TestResult.FromString,
                )
                with pytest.raises(grpc.RpcError) as error:
                    v1_call(service.GetTestResultRequest(test_result_id="test-id"), timeout=5)
                assert error.value.code() == grpc.StatusCode.UNIMPLEMENTED
        finally:
            server.stop(0).wait()
