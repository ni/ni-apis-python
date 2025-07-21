import logging

from google.protobuf import any_pb2

from ni.apis.python import GrpcClient
from ni.measurementlink.discovery.v1 import DiscoveryClient, discovery_service_pb2

from . import data_moniker_pb2, data_moniker_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MonikerClient(GrpcClient):
    DATA_STORE_SERVICE_CLASS = "ni.measurements.data.v1.DataStoreService"

    def __init__(self):
        super().__init__("Moniker")
        self._stub: data_moniker_pb2_grpc.MonikerServiceStub | None = None

    async def _get_service_location(self) -> discovery_service_pb2.ServiceLocation:
        discovery_client = DiscoveryClient()
        service_location = await discovery_client.resolve_service(
            self.DATA_STORE_SERVICE_CLASS,
            data_moniker_pb2.DESCRIPTOR.services_by_name["MonikerService"].full_name,
        )
        return service_location

    @GrpcClient.log_errors
    async def read_from_moniker(self, moniker: data_moniker_pb2.Moniker) -> any_pb2.Any:
        """Reads the value from the Moniker."""
        logger.info(f"Reading from moniker: {moniker}")

        stub = await self._get_stub()
        response = await stub.ReadFromMoniker(moniker)

        logger.info(f"Successfully read from moniker")

        return response.value

    async def _get_stub(self) -> data_moniker_pb2_grpc.MonikerServiceStub:
        if self._stub is None:
            channel = await self._get_or_create_channel()
            self._stub = data_moniker_pb2_grpc.MonikerServiceStub(channel)

        return self._stub
