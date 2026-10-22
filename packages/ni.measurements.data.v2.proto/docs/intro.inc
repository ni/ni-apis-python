Introduction
============

``ni.measurements.data.v2.proto`` provides generated protobuf messages and raw
gRPC service stubs for the NI Data Store V2 API. It supports CPython 3.10+ on
Windows and Linux and can be installed alongside the V1 proto package.

This is an unpublished development package. Build and install a local wheel;
no public PyPI release is available as part of this change.

Generation currently uses local datastore-service definitions. See the package
README for input fingerprints, generation instructions, and the required
upstream and CI integration before release.

The package does not implement server-side validation, a handwritten client,
or V2 service enablement. Calls require a compatible V2 server.
