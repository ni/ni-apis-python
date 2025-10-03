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
        # Read the file and find the version line
        $versionLine = Select-String -Path $pyprojectPath -Pattern '^\s*version\s*=\s*".*"' | Select-Object -First 1

        if ($versionLine) {
            # Extract the version string using regex
            if ($versionLine.Line -match 'version\s*=\s*"([^"]+)"') {
                $version = $matches[1]
                Write-Host "Package '$pkg' version: $version"
            } else {
                Write-Host "Package '$pkg': version line found but could not parse version."
            }
        } else {
            Write-Host "Package '$pkg': version line not found in pyproject.toml."
        }
    } else {
        Write-Host "Package '$pkg': pyproject.toml not found."
    }
}