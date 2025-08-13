$packages = @(
    "ni\measurementlink\discovery\v1"
    "ni\measurementlink\measurement\v2"
    "ni\measurementlink"
    "ni\measurementlink\pinmap\v1"
    "ni\protobuf\types"
)

$packages | Foreach-Object {
    & poetry run grpc-generator `
        --proto-basepath ..\..\third_party\ni-apis `
        --proto-subpath $_ `
        --output-basepath ..\..\packages\$($_ -replace '\\', '.')\src `
        --output-format subpackage
}
