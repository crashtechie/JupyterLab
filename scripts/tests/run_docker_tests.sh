#!/bin/bash
# Docker Container Security Test Runner
# Runs all security validation tests inside the Docker container

set -e  # Exit on error

echo "======================================================================="
echo "Docker Container Security Test Suite"
echo "Testing Issues #01-#05 Resolution"
echo "======================================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Start the test environment
echo "Starting Docker Compose test environment..."
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d

# Wait for container to be ready
echo "Waiting for container to be ready..."
sleep 5

# Check if container is running
if ! docker-compose -f docker-compose.yml -f docker-compose.test.yml ps | grep -q "Up"; then
    echo -e "${RED}✗ Container failed to start${NC}"
    docker-compose -f docker-compose.yml -f docker-compose.test.yml logs
    exit 1
fi

echo -e "${GREEN}✓ Container is running${NC}"
echo ""

# Run comprehensive security test
echo "======================================================================="
echo "Running Comprehensive Security Tests (Issues #01-#05)"
echo "======================================================================="
echo ""

docker-compose -f docker-compose.yml -f docker-compose.test.yml exec -T jupyter \
    python /home/jovyan/work/scripts/tests/test_docker_security_fixes.py

COMPREHENSIVE_EXIT_CODE=$?

echo ""
echo "======================================================================="
echo "Running Individual Test Suites"
echo "======================================================================="
echo ""

# Run path traversal tests
echo "-----------------------------------------------------------------------"
echo "Running Path Traversal Tests (Issue #04)"
echo "-----------------------------------------------------------------------"
docker-compose -f docker-compose.yml -f docker-compose.test.yml exec -T jupyter \
    python /home/jovyan/work/scripts/tests/test_path_traversal_fix.py

PATH_EXIT_CODE=$?

echo ""

# Run command injection tests
echo "-----------------------------------------------------------------------"
echo "Running Command Injection Tests (Issue #05)"
echo "-----------------------------------------------------------------------"
docker-compose -f docker-compose.yml -f docker-compose.test.yml exec -T jupyter \
    python /home/jovyan/work/scripts/tests/test_command_injection_fix.py

CMD_EXIT_CODE=$?

echo ""

# Summary
echo "======================================================================="
echo "TEST SUMMARY"
echo "======================================================================="

if [ $COMPREHENSIVE_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Comprehensive Security Tests (Issues #01-#05)"
else
    echo -e "${RED}✗ FAIL${NC}: Comprehensive Security Tests (Issues #01-#05)"
fi

if [ $PATH_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Path Traversal Tests (Issue #04)"
else
    echo -e "${RED}✗ FAIL${NC}: Path Traversal Tests (Issue #04)"
fi

if [ $CMD_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Command Injection Tests (Issue #05)"
else
    echo -e "${RED}✗ FAIL${NC}: Command Injection Tests (Issue #05)"
fi

echo "======================================================================="

# Cleanup option
echo ""
read -p "Keep containers running? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Stopping containers..."
    docker-compose -f docker-compose.yml -f docker-compose.test.yml down
    echo -e "${GREEN}✓ Containers stopped${NC}"
else
    echo ""
    echo "Containers still running. Access Jupyter Lab at: http://localhost:8888"
    echo "Token: test-token-for-validation"
    echo ""
    echo "To stop later, run:"
    echo "  docker-compose -f docker-compose.yml -f docker-compose.test.yml down"
fi

# Exit with appropriate code
if [ $COMPREHENSIVE_EXIT_CODE -eq 0 ] && [ $PATH_EXIT_CODE -eq 0 ] && [ $CMD_EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ ALL TESTS PASSED - Docker environment is secure${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ SOME TESTS FAILED - Review required${NC}"
    exit 1
fi
