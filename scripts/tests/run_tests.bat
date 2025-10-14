@echo off
REM Docker Compose Jupyter Lab Test Runner
REM This batch script runs the end-to-end tests for the Jupyter Lab setup

echo Starting Docker Compose Jupyter Lab End-to-End Tests
echo =====================================================

cd /d "%~dp0..\.."

REM Install required Python package for testing
echo Installing requests package in local Python environment...
python -m pip install requests

REM Run the test script
echo.
echo Running comprehensive tests...
python scripts\tests\test_docker_setup.py

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ All tests passed successfully!
    echo Your Docker Compose Jupyter Lab setup is working correctly.
) else (
    echo.
    echo ❌ Some tests failed. Check the results in scripts\tests\results\
    echo Review the test output above for details.
)

pause