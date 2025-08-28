"""Data types for the NI Discovery Service."""

from __future__ import annotations

import typing
from typing import NamedTuple

import ni.measurementlink.discovery.v1.discovery_service_pb2 as discovery_service_pb2


class ServiceInfo(NamedTuple):
    """A named tuple providing information about a registered service.

    This class is used with the NI Discovery Service when registering and enumerating services.
    """

    service_class: str
    """"The "class" of a service. The value of this field should be unique for all services.
    In effect, the ``.proto`` service declaration defines the interface, and this field
    defines a class or concrete type of the interface."""

    description_url: str
    """The URL of a web page that provides a description of the service."""

    provided_interfaces: list[str] = ["ni.measurementlink.measurement.v1.MeasurementService"]
    """The service interfaces provided by the service. These are gRPC full names for the service."""

    annotations: dict[str, str] = {}
    """Represents a set of annotations on the service.

    Well-known annotations:

    - Description
       - Key: "ni/service.description"
          - Expected format: string
          - Example: "Measure inrush current with a shorted load and validate results against
            configured limits."
    - Collection
       - Key: "ni/service.collection"
          - Expected format: "." delimited namespace/hierarchy case-insensitive string
          - Example: "CurrentTests.Inrush"
    - Tags
        - Key: "ni/service.tags"
           - Expected format: serialized JSON string of an array of strings
           - Example: "[\"powerup\", \"current\"]"
    """

    display_name: str = ""
    """The service display name for clients to display to users."""

    versions: list[str] = []
    """The list of versions associated with this service in
     the form major.minor.build[.revision] (e.g. 1.0.0)."""

    @classmethod
    def _from_grpc(cls, other: discovery_service_pb2.ServiceDescriptor) -> ServiceInfo:
        return ServiceInfo(
            service_class=other.service_class,
            description_url=other.description_url,
            provided_interfaces=list(other.provided_interfaces),
            annotations=dict(other.annotations),
            display_name=other.display_name,
            versions=list(other.versions),
        )


class ServiceLocation(typing.NamedTuple):
    """Represents the location of a service."""

    location: str
    insecure_port: str
    ssl_authenticated_port: str

    @property
    def insecure_address(self) -> str:
        """Get the service's insecure address in the format host:port."""
        return f"{self.location}:{self.insecure_port}"

    @property
    def ssl_authenticated_address(self) -> str:
        """Get the service's SSL-authenticated address in the format host:port."""
        return f"{self.location}:{self.ssl_authenticated_port}"

    @classmethod
    def _from_grpc(cls, other: discovery_service_pb2.ServiceLocation) -> ServiceLocation:
        return ServiceLocation(
            location=other.location,
            insecure_port=other.insecure_port,
            ssl_authenticated_port=other.ssl_authenticated_port,
        )


class ComputeNodeDescriptor(typing.NamedTuple):
    """Represents a compute node."""

    url: str
    """The resolvable name (URL) of the compute node."""

    is_local: bool
    """Indicates whether the compute node is local node."""

    @classmethod
    def _from_grpc(
        cls, other: discovery_service_pb2.ComputeNodeDescriptor
    ) -> ComputeNodeDescriptor:
        return ComputeNodeDescriptor(
            url=other.url,
            is_local=other.is_local,
        )
