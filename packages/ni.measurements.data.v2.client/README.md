# NI Data Store V2 gRPC client

`ni.measurements.data.v2.client` provides a synchronous, low-level Python
client for the NI Data Store V2 gRPC service. Its methods accept generated V2
protobuf request messages and return protobuf responses without converting
values into higher-level Python types.

The package depends on `ni.measurements.data.v2.proto` for generated messages
and stubs. It does not copy generated source and is not the high-level
`ni.datastore` API.

## Usage

```python
from ni.measurements.data.v2 import data_store_service_pb2
from ni.measurements.data.v2.client import DataStoreClient

request = data_store_service_pb2.GetMeasurementRequest(
    measurement_id="measurement-id"
)

with DataStoreClient() as client:
    measurement = client.get_measurement(request)
```

`DataStoreClient` exposes methods for the V2 service RPCs, including batch
operations. RPC errors are propagated to the caller.

## Connecting to the service

By default, the client lazily uses NI Discovery to locate the service and a
gRPC channel pool to obtain a channel. Applications can instead provide a
channel directly:

```python
import grpc
from ni.measurements.data.v2.client import DataStoreClient

channel = grpc.insecure_channel("localhost:50051")
try:
    with DataStoreClient(grpc_channel=channel) as client:
        ...
finally:
    channel.close()
```

When a channel is supplied, the application owns and closes it. The same
ownership principle applies to a caller-supplied channel pool. Resources created
by the client are cleaned up by `close()` or when leaving a `with` block.
Service discovery and a reachable, V2-enabled server are required when using
the default connection behavior.

## Development checks

From this package directory:

```powershell
poetry install --with docs
poetry run pytest -v
poetry run nps lint
poetry run mypy
poetry run pyright
poetry run bandit -c pyproject.toml -r src
poetry run sphinx-build docs docs\_build --builder html --fail-on-warning
poetry build
```

This is an unpublished development package. The V2 proto package is currently
generated from local datastore-service proto inputs and is not yet registered
in the repository's standard package generation and CI workflow.
