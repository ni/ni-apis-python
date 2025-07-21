import abc
import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Protocol, Self, Tuple

import grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceLocationType(Protocol):
    """Protocol defining the interface for service location objects."""

    def __init__(self, *, location: str, insecure_port: str, ssl_authenticated_port: str): ...

    @property
    def location(self) -> str: ...

    @property
    def insecure_port(self) -> str: ...

    @property
    def ssl_authenticated_port(self) -> str: ...


class GrpcClient(abc.ABC):
    def __init__(self, service_name: str, channel: grpc.aio.Channel | None = None):
        self._service_name = service_name
        self._channel_lock = asyncio.Lock()
        self._channel: grpc.aio.Channel | None = channel

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exec_tb):
        await self._close_channel()

    @abc.abstractmethod
    async def _get_service_location(self, *args, **kwargs) -> ServiceLocationType: ...

    async def _get_or_create_channel(self, reconnect: bool = False) -> grpc.aio.Channel:
        async with self._channel_lock:
            if self._channel and not reconnect:
                return self._channel

            await self.__close_channel_unsafe()
            self._channel, address = await self.__create_channel()
            logger.info(f"Created channel to {self._service_name} service at {address}")

        return self._channel

    async def _close_channel(self) -> None:
        async with self._channel_lock:
            await self.__close_channel_unsafe()

    async def __create_channel(self) -> Tuple[grpc.aio.Channel, str]:
        options = [
            ("grpc.max_receive_message_length", -1),
            ("grpc.max_send_message_length", -1),
        ]
        options.append(("grpc.enable_http_proxy", 0))

        service_location = await self._get_service_location()
        location = service_location.location.strip()
        insecure_port = service_location.insecure_port.strip()
        ssl_authenticated_port = service_location.ssl_authenticated_port.strip()
        if not insecure_port and not ssl_authenticated_port:
            raise ValueError(
                "ServiceLocation must have at least one port defined (insecure or SSL authenticated)"
            )
        if insecure_port:
            address = f"{location}:{insecure_port}"
            channel = grpc.aio.insecure_channel(address, options)
        else:
            address = f"{location}:{ssl_authenticated_port}"
            channel = grpc.aio.secure_channel(
                address, grpc.ssl_channel_credentials(), options=options
            )

        await channel.channel_ready()
        return channel, address

    async def __close_channel_unsafe(self):
        if self._channel is None:
            logger.info("Channel is already closed or not initialized")
            return

        try:
            await self._channel.close()
            logger.info(f"Closed gRPC channel to {self._service_name} service")
        except Exception as e:
            logger.error(f"Error while closing existing gRPC channel: {e}")
        finally:
            self._channel = None

    @staticmethod
    def log_errors(func: Callable) -> Callable:
        """Decorator that adds error logging to gRPC method calls."""

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except grpc.RpcError as e:
                logger.error(f"gRPC error: {e.code()} - {e.details()}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise

        return wrapper
