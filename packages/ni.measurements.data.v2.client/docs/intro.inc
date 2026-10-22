Introduction
============

The ``ni.measurements.data.v2.client`` package provides a synchronous,
low-level gRPC client for the NI Data Store Service V2. Methods accept V2
protobuf request messages and return protobuf responses.

Use the generated V2 proto package to create requests:

.. code-block:: python

   from ni.measurements.data.v2 import data_store_service_pb2
   from ni.measurements.data.v2.client import DataStoreClient

   request = data_store_service_pb2.GetMeasurementRequest()
   request.measurement_id = "measurement-id"

   with DataStoreClient() as client:
       measurement = client.get_measurement(request)

The client discovers the service when no gRPC channel is supplied. A caller
may supply a channel or channel pool; resources supplied by the caller remain
caller-owned. After ``close()`` returns, the client can be used again and will
create new connection resources as needed. If a channel or pool was supplied,
it remains open but is no longer used by the client after closing; a later call
discovers the service and creates new resources. Do not call ``close()`` while
RPCs are in progress. The service must be enabled and reachable to use the RPCs.

This package does not provide high-level value conversion or datastore
workflows; those belong to the separate ``ni.datastore`` package.
