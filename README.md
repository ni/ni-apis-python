# Table of Contents

- [Table of Contents](#table-of-contents)
- [About](#about)
  - [Operating System Support](#operating-system-support)
  - [Python Version Support](#python-version-support)

# About

`ni-apis-python` is a Git repository that provides Python packages for [NI's gRPC APIs](https://github.com/ni/ni-apis).

NI created and supports these packages.

- [`ni-grpc-extensions`](https://github.com/ni/ni-apis-python/tree/main/packages/ni-grpc-extensions) -- provides channel pool handling for gRPC communication
- [`ni.datamonikers.v1.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.datamonikers.v1.proto) -- provides Python stubs for the definitions in the `ni.datamonikers.v1` package. (.proto files at [ni/datamonikers/v1](https://github.com/ni/ni-apis/tree/main/ni/datamonikers/v1))
- [`ni.datamonikers.v1.client`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.datamonikers.v1.client) -- provides gRPC client code for the NI Data Moniker Service, version 1. The corresponding service is defined in the
`ni.datamonikers.v1.proto` package.
- [`ni.grpcdevice.v1.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.grpcdevice.v1.proto) -- provides stubs for definitions in the `nidevice_grpc` package. (.proto files at [ni/grpcdevice/v1](https://github.com/ni/ni-apis/tree/main/ni/grpcdevice/v1))
- [`ni.measurementlink.discovery.v1.client`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurementlink.discovery.v1.client) -- provides gRPC client code for the NI
Discovery Service, version 1. The corresponding service is defined in the
`ni.measurementlink.discovery.v1.proto` package.
- [`ni.measurementlink.discovery.v1.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurementlink.discovery.v1.proto) -- provides Python stubs for the definitions in the `ni.measurementlink.discovery.v1` package. (.proto files at [ni/measurementlink/discovery/v1](https://github.com/ni/ni-apis/tree/main/ni/measurementlink/discovery/v1))
- [`ni.measurementlink.measurement.v1.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurementlink.measurement.v1.proto) -- provides Python stubs for the definitions in the `ni.measurementlink.measurement.v1` package. (.proto files at [ni/measurementlink/measurement/v1](https://github.com/ni/ni-apis/tree/main/ni/measurementlink/measurement/v1))
- [`ni.measurementlink.measurement.v2.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurementlink.measurement.v2.proto) -- provides Python stubs for the definitions in the `ni.measurementlink.measurement.v2` package. (.proto files at [ni/measurementlink/measurement/v2](https://github.com/ni/ni-apis/tree/main/ni/measurementlink/measurement/v2))
- [`ni.measurementlink.pinmap.v1.client`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurementlink.pinmap.v1.client) -- provides gRPC client code for the NI Pin Map Service, version 1. The corresponding service is defined in the
`ni.measurementlink.pinmap.v1.proto` package.
- [`ni.measurementlink.pinmap.v1.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurementlink.pinmap.v1.proto) -- provides Python stubs for the definitions in the `ni.measurement.pinmap.v1` package. (.proto files at [ni/measurementlink/pinmap/v1](https://github.com/ni/ni-apis/tree/main/ni/measurementlink/pinmap/v1))
- [`ni.measurementlink.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurementlink.proto) -- provides Python stubs for the definitions in the `ni.measurementlink` package. (.proto files at [ni/measurementlink](https://github.com/ni/ni-apis/tree/main/ni/measurementlink))
- [`ni.measurementlink.sessionmanagement.v1.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurementlink.sessionmanagement.v1.proto) -- provides Python stubs for the definitions in the `ni.measurementlink.sessionmanagment.v1` package. (.proto files at [ni/measurementlink/sessionmanagement/v1](https://github.com/ni/ni-apis/tree/main/ni/measurementlink/sessionmanagement/v1))
- [`ni.measurements.metadata.v1.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.measurements.metadata.v1.proto) -- provides Python stubs for the definitions in the `ni.measurements.metadata.v1` package. (.proto files at [ni/measurements/metadata/v1](https://github.com/ni/ni-apis/tree/main/ni/measurements/metadata/v1))
- [`ni.panels.v1.proto`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.panels.v1.proto) -- provides Python stubs for the definitions in the `ni.panels.v1` package. (.proto files at [ni/panels/v1](https://github.com/ni/ni-apis/tree/main/ni/panels/v1))
- [`ni.protobuf.types`](https://github.com/ni/ni-apis-python/tree/main/packages/ni.protobuf.types) -- provides Python stubs for the definitions in the `ni.protobuf.types` package. (.proto files at [ni/protobuf/types](https://github.com/ni/ni-apis/tree/main/ni/protobuf/types))

## Operating System Support

`ni-apis-python` supports Windows and Linux operating systems.

## Python Version Support

`ni-apis-python` supports CPython 3.9+.
