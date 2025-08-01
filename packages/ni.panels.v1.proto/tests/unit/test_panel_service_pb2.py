from google.protobuf.any_pb2 import Any
from ni.panels.v1.panel_service_pb2 import (
    EnumeratePanelsRequest,
    EnumeratePanelsResponse,
    GetValueRequest,
    GetValueResponse,
    PanelInformation,
    SetValueRequest,
    SetValueResponse,
    StartPanelRequest,
    StartPanelResponse,
    StopPanelRequest,
    StopPanelResponse,
    TryGetValueRequest,
    TryGetValueResponse,
)
from ni.panels.v1.streamlit_panel_configuration_pb2 import StreamlitPanelConfiguration


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


def test___stop_panel_response___create___created_successfully() -> None:
    req = StopPanelResponse()

    assert isinstance(req, StopPanelResponse)


def test___enumerate_panels_request___create___created_successfully() -> None:
    req = EnumeratePanelsRequest()

    assert isinstance(req, EnumeratePanelsRequest)


def test___enumerate_panels_response___create___created_successfully() -> None:
    panel_info = PanelInformation(
        panel_id="panel_id",
        panel_url="some url",
        value_ids=["val1", "val2"],
    )
    req = EnumeratePanelsResponse(panels=[panel_info])

    panels = list(req.panels)
    assert len(panels) == 1
    assert panels[0].panel_id == "panel_id"
    assert panels[0].panel_url == "some url"
    assert panels[0].value_ids == ["val1", "val2"]


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


def test___set_value_response___create___created_successfully() -> None:
    req = SetValueResponse()

    assert isinstance(req, SetValueResponse)


def _get_configuration_as_any() -> Any:
    configuration = StreamlitPanelConfiguration(panel_script_url="path/to/panel.py")
    configuration_any = Any()
    configuration_any.Pack(configuration)
    return configuration_any
