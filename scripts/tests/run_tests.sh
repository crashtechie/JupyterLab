#!/bin/bash
# Docker Compose Jupyter Lab Test Runner for Linux/macOS
# This script runs end-to-end tests for the Jupyter Lab setup

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

echo -e "${CYAN}🧪 Starting Docker Compose Jupyter Lab End-to-End Tests${NC}"
echo -e "${CYAN}======================================================${NC}"

# Change to project root
cd "$PROJECT_ROOT"

# Function to print status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command_exists docker; then
    print_error "Docker is not installed or not in PATH"
    exit 1
fi

if ! command_exists python3; then
    if command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed or not in PATH"
        exit 1
    fi
else
    PYTHON_CMD="python3"
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
print_success "Found Python: $PYTHON_VERSION"

# Check Docker Compose
if docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command_exists docker-compose; then
    COMPOSE_CMD="docker-compose"
else
    print_error "Docker Compose is not available"
    exit 1
fi

COMPOSE_VERSION=$($COMPOSE_CMD version)
print_success "Found Docker Compose: $COMPOSE_VERSION"

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_NAME="Linux"
    PACKAGE_MANAGER=""
    
    # Detect Linux distribution and package manager
    if command_exists apt; then
        PACKAGE_MANAGER="apt"
    elif command_exists yum; then
        PACKAGE_MANAGER="yum"
    elif command_exists dnf; then
        PACKAGE_MANAGER="dnf"
    elif command_exists pacman; then
        PACKAGE_MANAGER="pacman"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_NAME="macOS"
    PACKAGE_MANAGER="brew"
else
    OS_NAME="Unknown Unix"
    PACKAGE_MANAGER=""
fi

print_status "Detected OS: $OS_NAME"

# Install required Python packages
print_status "Installing required Python packages..."

# Check if requests is available
if ! $PYTHON_CMD -c "import requests" 2>/dev/null; then
    print_warning "requests package not found, attempting to install..."
    
    # Try pip3 first, then pip
    if command_exists pip3; then
        pip3 install requests
    elif command_exists pip; then
        pip install requests
    else
        print_error "pip is not available. Please install the 'requests' package manually:"
        print_error "  $PYTHON_CMD -m pip install requests"
        exit 1
    fi
    
    print_success "requests package installed successfully"
else
    print_success "requests package is available"
fi

# Create virtual environment if needed (optional)
if [[ "${USE_VENV:-}" == "true" ]]; then
    print_status "Creating virtual environment..."
    VENV_DIR="${PROJECT_ROOT}/.test_venv"
    
    if [[ ! -d "$VENV_DIR" ]]; then
        $PYTHON_CMD -m venv "$VENV_DIR"
    fi
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    pip install requests
    print_success "Virtual environment activated"
fi

# Run the comprehensive test script
print_status "Running comprehensive Docker Compose tests..."
echo

if [[ -f "${SCRIPT_DIR}/test_docker_setup.py" ]]; then
    $PYTHON_CMD "${SCRIPT_DIR}/test_docker_setup.py"
    TEST_EXIT_CODE=$?
else
    print_error "Test script not found: ${SCRIPT_DIR}/test_docker_setup.py"
    exit 1
fi

echo
print_status "Test execution completed"

# Check results and provide feedback
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    print_success "All tests passed successfully! ✅"
    print_success "Your Docker Compose Jupyter Lab setup is working correctly."
    
    echo
    print_status "Next steps:"
    echo "  • Start Jupyter Lab: $COMPOSE_CMD up -d"
    echo "  • Access at: http://localhost:8888"
    echo "  • Token: datascience-token"
    echo "  • Stop services: $COMPOSE_CMD down"
    
else
    print_error "Some tests failed. ❌"
    print_error "Check the results in scripts/tests/results/"
    print_error "Review the test output above for details."
    
    echo
    print_status "Troubleshooting tips:"
    echo "  • Ensure Docker Desktop is running"
    echo "  • Check if ports are available (8888)"
    echo "  • Verify .env file exists and is configured"
    echo "  • Run 'docker compose config' to validate configuration"
fi

# OS-specific additional information
echo
print_status "OS-specific information:"

case "$OS_NAME" in
    "Linux")
        echo "  • Docker service: systemctl status docker"
        echo "  • Logs: journalctl -u docker"
        if [[ -n "$PACKAGE_MANAGER" ]]; then
            echo "  • Package manager: $PACKAGE_MANAGER"
        fi
        ;;
    "macOS")
        echo "  • Docker Desktop: Check Docker Desktop application"
        echo "  • Homebrew packages: brew list"
        echo "  • System info: sw_vers"
        ;;
    *)
        echo "  • Check your system's Docker documentation"
        ;;
esac

# Deactivate virtual environment if it was used
if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    deactivate
    print_status "Virtual environment deactivated"
fi

echo
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    print_success "🎉 Test execution completed successfully!"
    echo -e "${GREEN}Your Jupyter Lab environment is ready for data science work!${NC}"
else
    print_error "⚠️ Test execution completed with failures."
    echo -e "${RED}Please review the issues above before proceeding.${NC}"
fi

exit $TEST_EXIT_CODE