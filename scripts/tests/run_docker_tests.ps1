# Docker Container Security Test Runner (PowerShell)
# Runs all security validation tests inside the Docker container

$ErrorActionPreference = "Stop"

Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "Docker Container Security Test Suite" -ForegroundColor Cyan
Write-Host "Testing Issues #01-#05 Resolution" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info > $null 2>&1
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again"
    exit 1
}

Write-Host ""

# Start the test environment
Write-Host "Starting Docker Compose test environment..." -ForegroundColor Yellow
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d

# Wait for container to be ready
Write-Host "Waiting for container to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if container is running
$containerStatus = docker-compose -f docker-compose.yml -f docker-compose.test.yml ps
if ($containerStatus -notmatch "Up") {
    Write-Host "✗ Container failed to start" -ForegroundColor Red
    docker-compose -f docker-compose.yml -f docker-compose.test.yml logs
    exit 1
}

Write-Host "✓ Container is running" -ForegroundColor Green
Write-Host ""

# Run comprehensive security test
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "Running Comprehensive Security Tests (Issues #01-#05)" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

docker-compose -f docker-compose.yml -f docker-compose.test.yml exec -T jupyter python /home/jovyan/work/scripts/tests/test_docker_security_fixes.py
$comprehensiveExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "Running Individual Test Suites" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

# Run path traversal tests
Write-Host "-----------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "Running Path Traversal Tests (Issue #04)" -ForegroundColor Yellow
Write-Host "-----------------------------------------------------------------------" -ForegroundColor DarkGray
docker-compose -f docker-compose.yml -f docker-compose.test.yml exec -T jupyter python /home/jovyan/work/scripts/tests/test_path_traversal_fix.py
$pathExitCode = $LASTEXITCODE

Write-Host ""

# Run command injection tests
Write-Host "-----------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "Running Command Injection Tests (Issue #05)" -ForegroundColor Yellow
Write-Host "-----------------------------------------------------------------------" -ForegroundColor DarkGray
docker-compose -f docker-compose.yml -f docker-compose.test.yml exec -T jupyter python /home/jovyan/work/scripts/tests/test_command_injection_fix.py
$cmdExitCode = $LASTEXITCODE

Write-Host ""

# Summary
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan

if ($comprehensiveExitCode -eq 0) {
    Write-Host "✓ PASS: Comprehensive Security Tests (Issues #01-#05)" -ForegroundColor Green
} else {
    Write-Host "✗ FAIL: Comprehensive Security Tests (Issues #01-#05)" -ForegroundColor Red
}

if ($pathExitCode -eq 0) {
    Write-Host "✓ PASS: Path Traversal Tests (Issue #04)" -ForegroundColor Green
} else {
    Write-Host "✗ FAIL: Path Traversal Tests (Issue #04)" -ForegroundColor Red
}

if ($cmdExitCode -eq 0) {
    Write-Host "✓ PASS: Command Injection Tests (Issue #05)" -ForegroundColor Green
} else {
    Write-Host "✗ FAIL: Command Injection Tests (Issue #05)" -ForegroundColor Red
}

Write-Host "=======================================================================" -ForegroundColor Cyan

# Cleanup option
Write-Host ""
$keepRunning = Read-Host "Keep containers running? (y/n)"
if ($keepRunning -ne "y" -and $keepRunning -ne "Y") {
    Write-Host "Stopping containers..." -ForegroundColor Yellow
    docker-compose -f docker-compose.yml -f docker-compose.test.yml down
    Write-Host "✓ Containers stopped" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Containers still running. Access Jupyter Lab at: http://localhost:8888" -ForegroundColor Cyan
    Write-Host "Token: test-token-for-validation" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To stop later, run:" -ForegroundColor Yellow
    Write-Host "  docker-compose -f docker-compose.yml -f docker-compose.test.yml down" -ForegroundColor Yellow
}

# Exit with appropriate code
if ($comprehensiveExitCode -eq 0 -and $pathExitCode -eq 0 -and $cmdExitCode -eq 0) {
    Write-Host ""
    Write-Host "✅ ALL TESTS PASSED - Docker environment is secure" -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "❌ SOME TESTS FAILED - Review required" -ForegroundColor Red
    exit 1
}
