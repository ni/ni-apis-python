"""Client for accessing the NI Data Moniker Service."""

import threading
from typing import Iterator, Optional

import grpc
import ni.datamonikers.v1.data_moniker_pb2 as data_moniker_pb2
import ni.datamonikers.v1.data_moniker_pb2_grpc as data_moniker_pb2_grpc
from ni_grpc_extensions.channelpool import GrpcChannelPool


class MonikerClient:
    """Client for accessing the NI Data Moniker Service."""

    def __init__(
        self,
        *,
        uri: Optional[str] = None,
        grpc_channel: Optional[grpc.Channel] = None,
        grpc_channel_pool: Optional[GrpcChannelPool] = None,
    ) -> None:
        """Initialize the Moniker Client.

        Args:
            uri: A URI of the Data Moniker service location.

            grpc_channel: A data moniker gRPC channel.

            grpc_channel_pool: An optional gRPC channel pool (recommended).

        Either `uri` or `grpc_channel` must be provided. If both are provided,
        `grpc_channel` takes precedence.
        """
        if uri is None and grpc_channel is None:
            raise ValueError("Either 'uri' or 'grpc_channel' must be provided.")

        self._initialization_lock = threading.Lock()
        self._uri = uri
        self._grpc_channel_pool = grpc_channel_pool
        self._stub = (
            data_moniker_pb2_grpc.MonikerServiceStub(grpc_channel)
            if grpc_channel is not None
            else None
        )

    def _get_stub(self) -> data_moniker_pb2_grpc.MonikerServiceStub:
        if self._stub is None:
            with self._initialization_lock:
                if self._grpc_channel_pool is None:
                    self._grpc_channel_pool = GrpcChannelPool()

                channel = self._grpc_channel_pool.get_channel(self._uri)  # type: ignore
                self._stub = data_moniker_pb2_grpc.MonikerServiceStub(channel)

        return self._stub

    def begin_sideband_stream(
        self, request: data_moniker_pb2.BeginMonikerSidebandStreamRequest
    ) -> data_moniker_pb2.BeginMonikerSidebandStreamResponse:
        """Begin a sideband stream."""
        stub = self._get_stub()
        return stub.BeginSidebandStream(request)

    def stream_read(
        self, moniker_list: data_moniker_pb2.MonikerList
    ) -> Iterator[data_moniker_pb2.MonikerReadResult]:
        """Stream read data from monikers."""
        stub = self._get_stub()
        return stub.StreamRead(moniker_list)

    def stream_write(
        self, requests: Iterator[data_moniker_pb2.MonikerWriteRequest]
    ) -> Iterator[data_moniker_pb2.StreamWriteResponse]:
        """Stream write data to monikers."""
        stub = self._get_stub()
        return stub.StreamWrite(requests)

    def stream_read_write(
        self, requests: Iterator[data_moniker_pb2.MonikerWriteRequest]
    ) -> Iterator[data_moniker_pb2.MonikerReadResult]:
        """Stream read and write data with monikers."""
        stub = self._get_stub()
        return stub.StreamReadWrite(requests)

    def read_from_moniker(
        self, moniker: data_moniker_pb2.Moniker
    ) -> data_moniker_pb2.ReadFromMonikerResult:
        """Read data from a moniker."""
        stub = self._get_stub()
        return stub.ReadFromMoniker(moniker)

    def write_to_moniker(
        self, request: data_moniker_pb2.WriteToMonikerRequest
    ) -> data_moniker_pb2.WriteToMonikerResponse:
        """Write data to a moniker."""
        stub = self._get_stub()
        return stub.WriteToMoniker(request)
