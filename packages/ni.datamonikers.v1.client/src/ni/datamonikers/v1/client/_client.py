"""Client for accessing the NI Data Moniker Service."""

from __future__ import annotations

import logging
import sys
import threading
from types import TracebackType
from typing import TYPE_CHECKING, Iterator

import grpc
import ni.datamonikers.v1.data_moniker_pb2 as data_moniker_pb2
import ni.datamonikers.v1.data_moniker_pb2_grpc as data_moniker_pb2_grpc
from ni_grpc_extensions.channelpool import GrpcChannelPool

if TYPE_CHECKING:
    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self


_logger = logging.getLogger(__name__)


class MonikerClient:
    """Client for accessing the NI Data Moniker Service."""

    __slots__ = (
        "_lock",
        "_owns_grpc_channel_pool",
        "_service_location",
        "_grpc_channel_pool",
        "_stub",
    )

    _lock: threading.Lock
    _owns_grpc_channel_pool: bool
    _service_location: str | None
    _grpc_channel_pool: GrpcChannelPool | None
    _stub: data_moniker_pb2_grpc.MonikerServiceStub | None

    def __init__(
        self,
        *,
        service_location: str | None = None,
        grpc_channel: grpc.Channel | None = None,
        grpc_channel_pool: GrpcChannelPool | None = None,
    ) -> None:
        """Initialize the Moniker Client.

        Args:
            service_location: The address of the data moniker service location (recommended).

            grpc_channel: A data moniker gRPC channel (optional).

            grpc_channel_pool: A gRPC channel pool (recommended).

        Either `service_location` or `grpc_channel` must be provided. If both are provided,
        `grpc_channel` takes precedence.
        """
        if service_location is None and grpc_channel is None:
            raise ValueError("Either 'service_location' or 'grpc_channel' must be provided.")

        self._lock = threading.Lock()
        self._owns_grpc_channel_pool = False
        self._service_location = service_location
        self._grpc_channel_pool = grpc_channel_pool
        self._stub = (
            data_moniker_pb2_grpc.MonikerServiceStub(grpc_channel)
            if grpc_channel is not None
            else None
        )

    def __enter__(self) -> Self:
        """Enter the runtime context of the MonikerClient."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the runtime context of the MonikerClient."""
        self.close()

    def close(self) -> None:
        """Close the client and clean up resources that it owns."""
        with self._lock:
            self._stub = None
            if self._owns_grpc_channel_pool and self._grpc_channel_pool:
                self._grpc_channel_pool.close()
            self._grpc_channel_pool = None
            self._owns_grpc_channel_pool = False

    def _get_stub(self) -> data_moniker_pb2_grpc.MonikerServiceStub:
        if self._stub is None:
            with self._lock:
                if self._grpc_channel_pool is None:
                    _logger.debug("Creating unshared GrpcChannelPool.")
                    self._grpc_channel_pool = GrpcChannelPool()
                    self._owns_grpc_channel_pool = True

                if self._stub is None:
                    channel = self._grpc_channel_pool.get_channel(self._service_location)  # type: ignore
                    self._stub = data_moniker_pb2_grpc.MonikerServiceStub(channel)

        return self._stub

    def begin_sideband_stream(
        self, request: data_moniker_pb2.BeginMonikerSidebandStreamRequest
    ) -> data_moniker_pb2.BeginMonikerSidebandStreamResponse:
        """Begin a sideband stream."""
        return self._get_stub().BeginSidebandStream(request)

    def stream_read(
        self, moniker_list: data_moniker_pb2.MonikerList
    ) -> Iterator[data_moniker_pb2.MonikerReadResult]:
        """Stream read data from monikers."""
        return self._get_stub().StreamRead(moniker_list)

    def stream_write(
        self, requests: Iterator[data_moniker_pb2.MonikerWriteRequest]
    ) -> Iterator[data_moniker_pb2.StreamWriteResponse]:
        """Stream write data to monikers."""
        return self._get_stub().StreamWrite(requests)

    def stream_read_write(
        self, requests: Iterator[data_moniker_pb2.MonikerWriteRequest]
    ) -> Iterator[data_moniker_pb2.MonikerReadResult]:
        """Stream read and write data with monikers."""
        return self._get_stub().StreamReadWrite(requests)

    def read_from_moniker(
        self, moniker: data_moniker_pb2.Moniker
    ) -> data_moniker_pb2.ReadFromMonikerResult:
        """Read data from a moniker."""
        return self._get_stub().ReadFromMoniker(moniker)

    def write_to_moniker(
        self, request: data_moniker_pb2.WriteToMonikerRequest
    ) -> data_moniker_pb2.WriteToMonikerResponse:
        """Write data to a moniker."""
        return self._get_stub().WriteToMoniker(request)
