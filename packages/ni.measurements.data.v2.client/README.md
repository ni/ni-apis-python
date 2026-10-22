# NI Data Store V2 gRPC client

`ni.measurements.data.v2.client` provides a synchronous, low-level gRPC client
for the NI Data Store V2 service. It accepts V2 protobuf request messages and
returns protobuf responses without converting them into higher-level Python
types.

The client can use a gRPC channel supplied by the application or discover the
service through NI Discovery:

```python
from ni.measurements.data.v2 import data_store_service_pb2
from ni.measurements.data.v2.client import DataStoreClient

request = data_store_service_pb2.GetMeasurementRequest()
request.measurement_id = "measurement-id"

with DataStoreClient() as client:
    measurement = client.get_measurement(request)
```

To read the complete measurement value and optional limits, use
`client.read_measurement_values()` with a `ReadMeasurementValuesRequest`.
Its `read_mask` selects `value`, `upper_limit`, and/or `lower_limit`; an empty
mask selects all three. Check `response.HasField("upper_limit")` and
`response.HasField("lower_limit")` for presence. An unset limit can mean either
that it was not selected or that the measurement has no such limit.

The previous `read_measurement_value()` method and singular request/response
types have been replaced to match the updated, unpublished V2 proto contract.

The V2 service must be enabled and reachable for RPC calls to succeed. This
package does not provide a high-level datastore API or convert protobuf values.
