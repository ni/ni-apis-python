import logging

import grpc
from ni.measurementlink.discovery.v1.discovery_service_pb2 import ResolveServiceRequest
from ni.measurementlink.discovery.v1.discovery_service_pb2_grpc import DiscoveryServiceStub
from pytest import LogCaptureFixture

from ni_grpc_extensions.loggers import ClientLogger


def test___client_logger___logs_grpc_call(caplog: LogCaptureFixture) -> None:
    client_logger = ClientLogger()
    intercept_channel = grpc.intercept_channel(
        grpc.insecure_channel("localhost:12345"),
        client_logger,
    )
    stub = DiscoveryServiceStub(intercept_channel)
    with caplog.at_level(logging.DEBUG):
        try:
            stub.ResolveService(ResolveServiceRequest())
        except Exception:
            pass  # Expected: no server running

    method_name = "/ni.measurementlink.discovery.v1.DiscoveryService/ResolveService"
    debug_messages = [r.message for r in caplog.records if r.levelno == logging.DEBUG]
    assert any(method_name in msg for msg in debug_messages)
