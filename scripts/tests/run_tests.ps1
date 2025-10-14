# Docker Compose Jupyter Lab Test Runner (PowerShell)
# This PowerShell script runs the end-to-end tests for the Jupyter Lab setup

Write-Host "🧪 Starting Docker Compose Jupyter Lab End-to-End Tests" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

# Change to project root directory
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))

# Install required Python package for testing
Write-Host "`n📦 Installing requests package..." -ForegroundColor Yellow
try {
    & python -m pip install requests
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Requests package installed successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Warning: Could not install requests package" -ForegroundColor Yellow
    Write-Host "The test script may need internet connectivity" -ForegroundColor Yellow
}

# Run the test script
Write-Host "`n🚀 Running comprehensive tests..." -ForegroundColor Cyan
& python scripts\tests\test_docker_setup.py

# Check exit code and provide feedback
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ All tests passed successfully!" -ForegroundColor Green
    Write-Host "Your Docker Compose Jupyter Lab setup is working correctly." -ForegroundColor Green
} else {
    Write-Host "`n❌ Some tests failed." -ForegroundColor Red
    Write-Host "Check the results in scripts\tests\results\" -ForegroundColor Red
    Write-Host "Review the test output above for details." -ForegroundColor Red
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")