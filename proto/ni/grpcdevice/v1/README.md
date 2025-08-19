# Proto files

## `session.proto`

`session.proto` originally came from NI grpc-device. Its contents and relative file path
must match nimi-python, or else the `protobuf` will raise "duplicate symbol" errors. It
is checked into this Git repo in order to reuse the `Session` message in the `.proto`
files here.

Origin:
- Git repo: https://github.com/ni/nimi-python/blob/master/src/shared_protos/session.proto
- Commit hash: c9787038978642a257b85c452f097469369ad184
