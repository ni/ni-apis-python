"""Client for accessing the NI Metadata Store Service."""

import logging

GRPC_SERVICE_INTERFACE_NAME = "ni.measurements.metadata.v1.MetadataStoreService"
GRPC_SERVICE_CLASS = "ni.measurements.data.v1.DataStoreService"

_logger = logging.getLogger(__name__)


class MetadataStoreClient:
    """Client for accessing the NI Metadata Store Service."""
