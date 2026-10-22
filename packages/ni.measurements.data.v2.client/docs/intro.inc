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
caller-owned. The service must be enabled and reachable to use the RPCs.

This package does not provide high-level value conversion or datastore
workflows; those belong to the separate ``ni.datastore`` package.
