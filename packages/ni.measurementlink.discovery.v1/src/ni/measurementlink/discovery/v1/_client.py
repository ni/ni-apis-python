import json
import logging

from ni.apis.python import GrpcClient

from ni.measurementlink.discovery.v1._support import _get_nipath, _open_key_file

from . import discovery_service_pb2, discovery_service_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscoveryClient(GrpcClient):
    def __init__(self):
        super().__init__("Discovery")
        self._stub: discovery_service_pb2_grpc.DiscoveryServiceStub | None = None

    async def _get_service_location(self) -> discovery_service_pb2.ServiceLocation:
        version = discovery_service_pb2.DESCRIPTOR.package.split(".")[-1]
        key_file_path = (
            _get_nipath("NIPUBAPPDATADIR")
            / "MeasurementLink"
            / "Discovery"
            / version
            / "DiscoveryService.json"
        )
        with _open_key_file(str(key_file_path)) as key_file:
            key_json = json.load(key_file)
            return discovery_service_pb2.ServiceLocation(
                location="localhost", insecure_port=key_json["InsecurePort"]
            )

    @GrpcClient.log_errors
    async def resolve_service(
        self, service_class: str, provided_interface: str = ""
    ) -> discovery_service_pb2.ServiceLocation:
        logger.info(
            f"Resolving service class '{service_class}' and provided interface '{provided_interface}'"
        )

        stub = await self._get_stub()
        request = discovery_service_pb2.ResolveServiceRequest(
            service_class=service_class,
            provided_interface=provided_interface,
        )
        response = await stub.ResolveService(request)

        logger.info(
            f"Resolved service class '{service_class}' and provided interface '{provided_interface}' to: {response}"
        )

        return response

    async def _get_stub(self) -> discovery_service_pb2_grpc.DiscoveryServiceStub:
        if self._stub is None:
            channel = await self._get_or_create_channel()
            self._stub = discovery_service_pb2_grpc.DiscoveryServiceStub(channel)

        return self._stub
