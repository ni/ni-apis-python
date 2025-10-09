from __future__ import annotations

import logging
import sys
import threading
from types import TracebackType
from typing import TYPE_CHECKING, Generic, Protocol, TypeVar

import grpc
from ni.measurementlink.discovery.v1.client import DiscoveryClient
from ni_grpc_extensions.channelpool import GrpcChannelPool

if TYPE_CHECKING:
    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

_logger = logging.getLogger(__name__)


class StubProtocol(Protocol):
    """Protocol for gRPC stub classes."""

    def __init__(self, channel: grpc.Channel) -> None:
        """Initialize the gRPC client."""


TStub = TypeVar("TStub", bound=StubProtocol)


class GrpcServiceClientBase(Generic[TStub]):
    """Base class for NI gRPC service clients."""

    __slots__ = (
        "_lock",
        "_owns_grpc_channel_pool",
        "_discovery_client",
        "_grpc_channel_pool",
        "_stub",
        "_service_interface_name",
        "_service_class",
        "_stub_class",
    )

    _lock: threading.Lock
    _owns_grpc_channel_pool: bool
    _discovery_client: DiscoveryClient | None
    _grpc_channel_pool: GrpcChannelPool | None
    _stub: TStub | None
    _service_interface_name: str
    _service_class: str
    _stub_class: type[TStub]

    def __init__(
        self,
        service_interface_name: str,
        service_class: str,
        stub_class: type[TStub],
        *,
        discovery_client: DiscoveryClient | None = None,
        grpc_channel: grpc.Channel | None = None,
        grpc_channel_pool: GrpcChannelPool | None = None,
    ) -> None:
        """Initialize the gRPC client.

        Args:
            service_interface_name: The fully qualified name of the service interface.
            service_class: The name of the service class.
            stub_class: The gRPC stub class for the service.
            discovery_client: An optional discovery client (recommended).
            grpc_channel: An optional pin map gRPC channel.
            grpc_channel_pool: An optional gRPC channel pool (recommended).
        """
        self._lock = threading.Lock()
        self._owns_grpc_channel_pool = False
        self._discovery_client = discovery_client
        self._grpc_channel_pool = grpc_channel_pool
        self._stub = stub_class(grpc_channel) if grpc_channel is not None else None
        self._service_interface_name = service_interface_name
        self._service_class = service_class
        self._stub_class = stub_class

    def __enter__(self) -> Self:
        """Enter the runtime context of the GrpcServiceClientBase."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the runtime context of the GrpcServiceClientBase."""
        self.close()

    def close(self) -> None:
        """Close the client and clean up resources that it owns."""
        with self._lock:
            self._stub = None
            self._discovery_client = None
            if self._owns_grpc_channel_pool and self._grpc_channel_pool:
                self._grpc_channel_pool.close()
            self._grpc_channel_pool = None
            self._owns_grpc_channel_pool = False

    def _get_stub(self) -> TStub:
        if self._stub is None:
            with self._lock:
                if self._grpc_channel_pool is None:
                    _logger.debug("Creating unshared GrpcChannelPool.")
                    self._grpc_channel_pool = GrpcChannelPool()
                    self._owns_grpc_channel_pool = True

                if self._discovery_client is None:
                    _logger.debug("Creating unshared DiscoveryClient.")
                    self._discovery_client = DiscoveryClient(
                        grpc_channel_pool=self._grpc_channel_pool
                    )

                if self._stub is None:
                    compute_nodes = self._discovery_client.enumerate_compute_nodes()
                    remote_nodes = [node for node in compute_nodes if not node.is_local]
                    target_url = remote_nodes[0].url if len(remote_nodes) == 1 else ""

                    service_location = self._discovery_client.resolve_service(
                        provided_interface=self._service_interface_name,
                        deployment_target=target_url,
                        service_class=self._service_class,
                    )

                    channel = self._grpc_channel_pool.get_channel(service_location.insecure_address)
                    self._stub = self._stub_class(channel)

        return self._stub
