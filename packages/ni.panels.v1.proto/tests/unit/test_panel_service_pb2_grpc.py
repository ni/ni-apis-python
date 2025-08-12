import grpc

import ni.panels.v1.panel_service_pb2_grpc


def test___panel_service_stub___contains_correct_methods() -> None:
    # Create a dummy channel using grpc.insecure_channel (won't connect)
    stub = ni.panels.v1.panel_service_pb2_grpc.PanelServiceStub(
        grpc.insecure_channel("localhost:12345")
    )

    assert hasattr(stub, "StartPanel")
    assert hasattr(stub, "StopPanel")
    assert hasattr(stub, "EnumeratePanels")
    assert hasattr(stub, "GetValue")
    assert hasattr(stub, "TryGetValue")
    assert hasattr(stub, "SetValue")


def test_add_servicer_to_server_exists() -> None:
    assert hasattr(ni.panels.v1.panel_service_pb2_grpc, "add_PanelServiceServicer_to_server")
