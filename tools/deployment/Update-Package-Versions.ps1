# Desired version to set
$newVersion = "1.2.3.dev0"

# Full list of package directories
$packages = @(
    "ni.datamonikers.v1.client",
    "ni.datamonikers.v1.proto",
    "ni.grpcdevice.v1.proto",
    "ni.measurementlink.discovery.v1.client",
    "ni.measurementlink.discovery.v1.proto",
    "ni.measurementlink.measurement.v1.proto",
    "ni.measurementlink.measurement.v2.proto",
    "ni.measurementlink.pinmap.v1.client",
    "ni.measurementlink.pinmap.v1.proto",
    "ni.measurementlink.proto",
    "ni.measurementlink.sessionmanagement.v1.client",
    "ni.measurementlink.sessionmanagement.v1.proto",
    "ni.measurements.data.v1.client",
    "ni.measurements.data.v1.proto",
    "ni.measurements.metadata.v1.client",
    "ni.measurements.metadata.v1.proto",
    "ni.panels.v1.proto",
    "ni.protobuf.types",
    "ni-grpc-extensions"
)

foreach ($pkg in $packages) {
    $pyprojectPath = "../../packages/$pkg/pyproject.toml"

    if (Test-Path $pyprojectPath) {
        $content = Get-Content $pyprojectPath

        # Replace the version line
        $updatedContent = $content | ForEach-Object {
            if ($_ -match '^\s*version\s*=\s*"[^"]*"') {
                "version = `"$newVersion`""
            } else {
                $_
            }
        }

        # Write the updated content back to the file
        $updatedContent | Set-Content $pyprojectPath

        Write-Host "Updated version for '$pkg' to $newVersion"
    } else {
        Write-Host "Package '$pkg': pyproject.toml not found."
    }
}
