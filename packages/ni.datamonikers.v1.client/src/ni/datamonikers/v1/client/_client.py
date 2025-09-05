"""Client for accessing the NI Data Moniker Service."""

import logging

GRPC_SERVICE_INTERFACE_NAME = "ni.datamonikers.v1.MonikerService"
GRPC_SERVICE_CLASS = "ni.datamonikers.v1.MonikerService"

_logger = logging.getLogger(__name__)


class MonikerClient:
    """Client for accessing the NI Data Moniker Service."""
