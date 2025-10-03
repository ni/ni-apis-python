# List of package directories.
# Keeping it small for now so we don't
# do too much damage during testing
# and create a ridiculous number of releases.
$packages = @(
    "ni.datamonikers.v1.client",
    "ni.measurements.metadata.v1.client",
    "ni.measurements.metadata.v1.proto"
)

foreach ($pkg in $packages) {
    $pyprojectPath = "../../packages/$pkg/pyproject.toml"

    if (Test-Path $pyprojectPath) {
        $versionLine = Select-String -Path $pyprojectPath -Pattern '^\s*version\s*=\s*".*"' | Select-Object -First 1

        if ($versionLine -and $versionLine.Line -match 'version\s*=\s*"([^"]+)"') {
            $version = $matches[1]
            $tag = "test-delete-$pkg-v$version"
            $title = "$pkg v$version"

            # Check if tag already exists
            $existingTags = git tag
            if ($existingTags -contains $tag) {
                Write-Host "Tag '$tag' already exists. Skipping release for '$pkg'."
                continue
            }

            Write-Host "Creating draft release for '$pkg' with tag '$tag'..."

            # Create draft release using GitHub CLI
            gh release create $tag `
                --title "$title" `
                --notes "Draft release for $pkg version $version" `
                --draft
        } else {
            Write-Host "Package '$pkg': version not found or could not be parsed."
        }
    } else {
        Write-Host "Package '$pkg': pyproject.toml not found."
    }
}