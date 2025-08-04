import google.protobuf.any_pb2 as any_pb2
from typing_extensions import assert_type
import ni.panels.v1.panel_service_pb2
from ni.panels.v1.panel_service_pb2 import (
    EnumeratePanelsResponse,
    GetValueRequest,
    GetValueResponse,
    PanelInformation,
    SetValueRequest,
    StartPanelRequest,
    StartPanelResponse,
    StopPanelRequest,
    TryGetValueRequest,
    TryGetValueResponse,
)
from ni.panels.v1.streamlit_panel_configuration_pb2 import StreamlitPanelConfiguration


def test___panel_service_module___check_messages___has_correct_messages() -> None:
    expected_message_types = [
        "EnumeratePanelsRequest",
        "EnumeratePanelsResponse",
        "GetValueRequest",
        "GetValueResponse",
        "PanelInformation",
        "SetValueRequest",
        "SetValueResponse",
        "StartPanelRequest",
        "StartPanelResponse",
        "StopPanelRequest",
        "StopPanelResponse",
        "TryGetValueRequest",
        "TryGetValueResponse",
    ]
    for message_type in expected_message_types:
        assert hasattr(ni.panels.v1.panel_service_pb2, message_type)


def test___start_panel_request___create___created_successfully() -> None:
    configuration_any = _get_configuration_as_any()

    req = StartPanelRequest(panel_id="test_panel", panel_configuration=configuration_any)

    assert req.panel_id == "test_panel"
    assert req.HasField("panel_configuration")


def test___start_panel_response___create___created_successfully() -> None:
    req = StartPanelResponse(panel_url="some_url")

    assert req.panel_url == "some_url"


def test___stop_panel_request___create___created_successfully() -> None:
    req = StopPanelRequest(panel_id="test_panel", reset=True)

    assert req.panel_id == "test_panel"
    assert req.reset is True


def test___enumerate_panels_response___create___created_successfully() -> None:
    panel_info = PanelInformation(
        panel_id="panel_id",
        panel_url="some url",
        value_ids=["val1", "val2"],
    )
    req = EnumeratePanelsResponse(panels=[panel_info])

    assert len(req.panels) == 1
    panel_info = req.panels[0]
    assert_type(panel_info, PanelInformation)
    assert isinstance(panel_info, PanelInformation)
    assert panel_info.panel_id == "panel_id"
    assert panel_info.panel_url == "some url"
    assert panel_info.value_ids == ["val1", "val2"]


def test___get_value_request___create___created_successfully() -> None:
    req = GetValueRequest(panel_id="test_panel", value_id="test_value")

    assert req.panel_id == "test_panel"
    assert req.value_id == "test_value"


def test___get_value_response___create___created_successfully() -> None:
    value_any = _get_configuration_as_any()
    req = GetValueResponse(value=value_any)

    assert req.HasField("value")


def test___try_get_value_request___create___created_successfully() -> None:
    req = TryGetValueRequest(panel_id="test_panel", value_id="test_value")

    assert req.panel_id == "test_panel"
    assert req.value_id == "test_value"


def test___try_get_value_response___create___created_successfully() -> None:
    value_any = _get_configuration_as_any()

    req = TryGetValueResponse(value=value_any)

    assert req.HasField("value")


def test___set_value_request___create___created_successfully() -> None:
    value_any = _get_configuration_as_any()
    req = SetValueRequest(
        panel_id="test_panel",
        value_id="val1",
        value=value_any,
        notify=True,
    )

    assert req.panel_id == "test_panel"
    assert req.value_id == "val1"
    assert req.HasField("value")
    assert req.notify is True


def _get_configuration_as_any() -> any_pb2.Any:
    configuration = StreamlitPanelConfiguration(panel_script_url="path/to/panel.py")
    configuration_any = any_pb2.Any()
    configuration_any.Pack(configuration)
    return configuration_any
