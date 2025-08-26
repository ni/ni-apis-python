"""Public API for accessing the NI Discovery Service."""

from ni.measurementlink.discovery.v1.client._client import DiscoveryClient
from ni.measurementlink.discovery.v1.client._info import ServiceInfo
from ni.measurementlink.discovery.v1.client._types import (
    ComputeNodeDescriptor,
    ServiceLocation,
)

__all__ = ["DiscoveryClient", "ServiceLocation", "ComputeNodeDescriptor", "ServiceInfo"]
