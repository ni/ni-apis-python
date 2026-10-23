# Table of Contents

- [Table of Contents](#table-of-contents)
- [About](#about)
  - [Operating System Support](#operating-system-support)
  - [Python Version Support](#python-version-support)
- [Asynchronous gRPC calls](#asynchronous-grpc-calls)
- [Installation](#installation)

# About

`ni.measurements.data.v2.proto` is a Python package that provides data types
and service stubs for the NI Data Store V2 gRPC API.

NI created and supports this package.

## Asynchronous gRPC calls

For asynchronous calls, construct `DataStoreServiceStub` with a
`grpc.aio.Channel`:

```python
import grpc
from ni.measurements.data.v2 import data_store_service_pb2
from ni.measurements.data.v2.data_store_service_pb2_grpc import DataStoreServiceStub


async def get_measurement():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = DataStoreServiceStub(channel)
        return await stub.GetMeasurement(
            data_store_service_pb2.GetMeasurementRequest(
                measurement_id="measurement-id"
            )
        )
```

`DataStoreServiceAsyncStub` is available only for type checking; it cannot be
imported at runtime.

## Operating System Support

`ni.measurements.data.v2.proto` supports Windows and Linux operating systems.

## Python Version Support

`ni.measurements.data.v2.proto` supports CPython 3.10+.

## Installation

You can directly install the `ni.measurements.data.v2.proto` package using
`pip` or by listing it as a dependency in your project's `pyproject.toml` file.
