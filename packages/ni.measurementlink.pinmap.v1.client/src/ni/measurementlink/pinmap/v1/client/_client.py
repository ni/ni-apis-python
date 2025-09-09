"""Client for accessing the NI Pin Map Service."""

from __future__ import annotations

import pathlib

import grpc
import ni.measurementlink.pinmap.v1.pin_map_service_pb2 as pin_map_service_pb2
from ni.measurementlink.discovery.v1.client import DiscoveryClient
from ni.measurementlink.pinmap.v1 import pin_map_service_pb2_grpc
from ni_grpc_extensions.channelpool import GrpcChannelPool

from ni.measurementlink.pinmap.v1.client._client_base import GrpcServiceClientBase


class PinMapClient(GrpcServiceClientBase):
    """Client for accessing the NI Pin Map Service via gRPC."""

    def __init__(
        self,
        *,
        discovery_client: DiscoveryClient | None = None,
        grpc_channel: grpc.Channel | None = None,
        grpc_channel_pool: GrpcChannelPool | None = None,
    ) -> None:
        """Initialize a PinMapClient instance."""
        super().__init__(
            discovery_client=discovery_client,
            grpc_channel=grpc_channel,
            grpc_channel_pool=grpc_channel_pool,
            service_interface_name="ni.measurementlink.pinmap.v1.PinMapService",
            service_class="ni.measurementlink.pinmap.v1.PinMapService",
            stub_class=pin_map_service_pb2_grpc.PinMapServiceStub,
        )

    def update_pin_map(self, pin_map_path: str | pathlib.Path) -> str:
        """Update the pin map from an XML file and return the pin map ID."""
        request = pin_map_service_pb2.UpdatePinMapFromXmlRequest(
            pin_map_id=str(pin_map_path),
            pin_map_xml=pathlib.Path(pin_map_path).read_text(encoding="utf-8-sig"),
        )
        stub: pin_map_service_pb2_grpc.PinMapServiceStub = self._get_stub()  # type: ignore
        response = stub.UpdatePinMapFromXml(request)
        return str(response.pin_map_id)
