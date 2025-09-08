"""Client for accessing the NI Data Store Service."""

import logging

GRPC_SERVICE_INTERFACE_NAME = "ni.measurements.data.v1.DataStoreService"
GRPC_SERVICE_CLASS = "ni.measurements.data.v1.DataStoreService"

_logger = logging.getLogger(__name__)


class DataStoreClient:
    """Client for accessing the NI Data Store Service."""
