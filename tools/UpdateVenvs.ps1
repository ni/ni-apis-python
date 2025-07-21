# Script to update virtual environments for all packages
# This script deletes existing .venv directories and recreates them with poetry install

$packagesPath = "$PSScriptRoot/../packages"
$packagesToUpdate = @()

Write-Host "Scanning for packages with .venv directories..." -ForegroundColor Cyan

# Find all package directories that have .venv folders
Get-ChildItem -Path $packagesPath -Directory | ForEach-Object {
    $packagePath = $_.FullName
    $venvPath = Join-Path $packagePath ".venv"

    if (Test-Path $venvPath) {
        Write-Host "Found .venv in: $($_.Name)" -ForegroundColor Yellow
        $packagesToUpdate += $packagePath

        # Delete the .venv directory
        Write-Host "  Deleting .venv directory..." -ForegroundColor Red
        try {
            Remove-Item $venvPath -Recurse -Force -ErrorAction Stop
            Write-Host "  .venv deleted successfully" -ForegroundColor Green
        }
        catch {
            Write-Host "  ERROR: Failed to delete .venv directory: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "Script terminated due to deletion failure." -ForegroundColor Red
            exit 1
        }
    }
}

if ($packagesToUpdate.Count -eq 0) {
    Write-Host "No .venv directories found in packages." -ForegroundColor Green
    exit 0
}

Write-Host "`nRunning poetry install for updated packages..." -ForegroundColor Cyan

# Run poetry install in each package that had .venv deleted
foreach ($packagePath in $packagesToUpdate) {
    $packageName = Split-Path $packagePath -Leaf
    Write-Host "`nProcessing package: $packageName" -ForegroundColor Magenta

    # Change to package directory
    Push-Location $packagePath

    try {
        # Run poetry install
        Write-Host "  Running poetry install..." -ForegroundColor Yellow
        poetry install

        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Poetry install completed successfully" -ForegroundColor Green
        }
        else {
            Write-Host "  Poetry install failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "  Error running poetry install: $($_.Exception.Message)" -ForegroundColor Red
    }
    finally {
        # Return to original directory
        Pop-Location
    }
}

Write-Host "`nScript completed!" -ForegroundColor Cyan
