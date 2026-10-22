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

The V2 service must be enabled and reachable for RPC calls to succeed. This
package does not provide a high-level datastore API or convert protobuf values.
