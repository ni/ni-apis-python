"""Service info class."""

from __future__ import annotations

from typing import NamedTuple

from ni.measurementlink.discovery.v1 import discovery_service_pb2


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
