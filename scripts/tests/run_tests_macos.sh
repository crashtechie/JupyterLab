#!/bin/bash
# Docker Compose Jupyter Lab Test Runner - macOS Optimized
# This script runs end-to-end tests with macOS-specific optimizations

set -e  # Exit on any error

# Colors for output (macOS Terminal compatible)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

echo -e "${CYAN}🍎 Docker Compose Jupyter Lab Tests - macOS Edition${NC}"
echo -e "${CYAN}===================================================${NC}"

# Change to project root
cd "$PROJECT_ROOT"

# Function to print status messages with macOS style
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ [SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️  [WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}❌ [ERROR]${NC} $1"
}

print_macos() {
    echo -e "${PURPLE}🍎 [macOS]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# macOS System Information
print_macos "Gathering macOS system information..."
MACOS_VERSION=$(sw_vers -productVersion)
MACOS_BUILD=$(sw_vers -buildVersion)
ARCH=$(uname -m)

print_success "macOS Version: $MACOS_VERSION (Build: $MACOS_BUILD)"
print_success "Architecture: $ARCH"

# Check if running on Apple Silicon
if [[ "$ARCH" == "arm64" ]]; then
    print_macos "Detected Apple Silicon (M1/M2/M3) - Using ARM64 optimizations"
    DOCKER_PLATFORM="--platform linux/arm64"
else
    print_macos "Detected Intel Mac - Using x86_64 platform"
    DOCKER_PLATFORM="--platform linux/amd64"
fi

# Check Homebrew installation
if command_exists brew; then
    BREW_VERSION=$(brew --version | head -n1)
    print_success "Homebrew available: $BREW_VERSION"
    
    # Check for common Homebrew-installed tools
    if brew list python@3.12 >/dev/null 2>&1; then
        PYTHON_CMD="/opt/homebrew/bin/python3.12"
        print_macos "Using Homebrew Python 3.12"
    elif brew list python@3.11 >/dev/null 2>&1; then
        PYTHON_CMD="/opt/homebrew/bin/python3.11"
        print_macos "Using Homebrew Python 3.11"
    elif command_exists python3; then
        PYTHON_CMD="python3"
    else
        print_warning "Python3 not found in Homebrew, using system Python"
        PYTHON_CMD="python3"
    fi
else
    print_warning "Homebrew not found. Consider installing: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    PYTHON_CMD="python3"
fi

# Check prerequisites
print_status "Checking prerequisites..."

# Check Docker Desktop for Mac
if ! command_exists docker; then
    print_error "Docker is not installed. Install Docker Desktop for Mac:"
    print_error "  https://docs.docker.com/desktop/mac/install/"
    exit 1
fi

# Check if Docker Desktop is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker Desktop is not running. Please start Docker Desktop."
    print_error "  You can find it in Applications/Docker.app"
    exit 1
fi

DOCKER_VERSION=$(docker --version)
print_success "Docker: $DOCKER_VERSION"

# Check Docker Compose (macOS typically uses 'docker compose')
if docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command_exists docker-compose; then
    COMPOSE_CMD="docker-compose"
    print_warning "Using legacy docker-compose. Consider upgrading to Docker Compose V2"
else
    print_error "Docker Compose is not available"
    exit 1
fi

COMPOSE_VERSION=$($COMPOSE_CMD version)
print_success "Docker Compose: $COMPOSE_VERSION"

# Check Python
if ! command_exists "$PYTHON_CMD"; then
    print_error "Python is not available. Install with Homebrew:"
    print_error "  brew install python@3.12"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
print_success "Python: $PYTHON_VERSION"

# macOS-specific checks
print_macos "Performing macOS-specific checks..."

# Check available memory (macOS uses different commands)
MEMORY_GB=$(system_profiler SPHardwareDataType | grep "Memory:" | awk '{print $2, $3}')
print_macos "System Memory: $MEMORY_GB"

# Check available disk space
DISK_AVAILABLE=$(df -h / | awk 'NR==2{print $4}')
print_macos "Available Disk Space: $DISK_AVAILABLE"

# Check if VirtualBox or VMware is running (can conflict with Docker)
if pgrep -x "VirtualBox" >/dev/null 2>&1; then
    print_warning "VirtualBox is running - this may cause conflicts with Docker Desktop"
fi

if pgrep -x "vmware" >/dev/null 2>&1; then
    print_warning "VMware is running - this may cause conflicts with Docker Desktop"
fi

# Install required Python packages
print_status "Setting up Python environment..."

# Create a temporary requirements file for macOS
cat > /tmp/macos_requirements.txt << EOF
requests>=2.25.0
urllib3>=1.26.0
certifi>=2021.5.25
EOF

# Install packages with macOS-specific considerations
if command_exists pip3; then
    print_status "Installing Python packages..."
    pip3 install --user -r /tmp/macos_requirements.txt
    print_success "Python packages installed successfully"
else
    print_error "pip3 not found. Install with: $PYTHON_CMD -m ensurepip --upgrade"
    exit 1
fi

# Clean up temporary file
rm -f /tmp/macos_requirements.txt

# Check for common macOS Docker issues
print_macos "Checking for common macOS Docker issues..."

# Check if Docker has sufficient resources allocated
DOCKER_MEM=$(docker info --format '{{.MemTotal}}' 2>/dev/null || echo "0")
if [[ "$DOCKER_MEM" -lt 2147483648 ]]; then  # 2GB in bytes
    print_warning "Docker Desktop may have insufficient memory allocated"
    print_warning "Increase memory in Docker Desktop Preferences > Resources"
fi

# Check file sharing settings
if [[ ! -w "$PROJECT_ROOT" ]]; then
    print_warning "Project directory may not be accessible to Docker"
    print_warning "Check Docker Desktop Preferences > Resources > File Sharing"
fi

# Export DOCKER_BUILDKIT for better performance on macOS
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

print_macos "Enabled Docker BuildKit for improved performance"

# Run the comprehensive test script
print_status "Running comprehensive Docker Compose tests..."
echo

# Set macOS-specific environment variables
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES  # Helps with multiprocessing on macOS

if [[ -f "${SCRIPT_DIR}/test_docker_setup.py" ]]; then
    $PYTHON_CMD "${SCRIPT_DIR}/test_docker_setup.py"
    TEST_EXIT_CODE=$?
else
    print_error "Test script not found: ${SCRIPT_DIR}/test_docker_setup.py"
    exit 1
fi

echo
print_status "Test execution completed"

# Check results and provide macOS-specific feedback
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    print_success "All tests passed successfully! 🎉"
    print_success "Your Docker Compose Jupyter Lab setup is working correctly on macOS."
    
    echo
    print_macos "macOS-optimized commands:"
    echo "  • Start Jupyter Lab: $COMPOSE_CMD up -d"
    echo "  • Access at: http://localhost:8888"
    echo "  • Token: datascience-token"
    echo "  • Stop services: $COMPOSE_CMD down"
    echo "  • View logs: $COMPOSE_CMD logs -f jupyter"
    
    # macOS-specific performance tips
    echo
    print_macos "Performance tips for macOS:"
    echo "  • Use named volumes for better performance"
    echo "  • Enable 'Use gRPC FUSE for file sharing' in Docker Desktop"
    echo "  • Allocate sufficient CPU/Memory in Docker Desktop settings"
    
else
    print_error "Some tests failed. ❌"
    print_error "Check the results in scripts/tests/results/"
    
    echo
    print_macos "macOS troubleshooting:"
    echo "  • Restart Docker Desktop: osascript -e 'quit app \"Docker\"' && open -a Docker"
    echo "  • Check Docker Desktop logs: ~/Library/Containers/com.docker.docker/Data/log/"
    echo "  • Verify file sharing permissions in Docker Desktop preferences"
    echo "  • Check Activity Monitor for resource usage"
    
    # Check for common macOS issues
    if [[ "$ARCH" == "arm64" ]]; then
        echo "  • Apple Silicon note: Some images may need --platform linux/amd64"
    fi
fi

# macOS system integration
echo
print_macos "System integration notes:"
echo "  • Docker Desktop: /Applications/Docker.app"
echo "  • Container logs: Docker Desktop > Containers tab"
echo "  • System resources: Activity Monitor"
echo "  • Network diagnostics: Docker Desktop > Troubleshoot"

# Create macOS-specific shortcuts
SHORTCUTS_DIR="$HOME/Desktop/JupyterLab-Shortcuts"
if [[ ! -d "$SHORTCUTS_DIR" ]]; then
    mkdir -p "$SHORTCUTS_DIR"
    
    # Create AppleScript to start Jupyter Lab
    cat > "$SHORTCUTS_DIR/Start Jupyter Lab.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/../../../JupyterLab"
docker compose up -d
sleep 3
open "http://localhost:8888/lab?token=datascience-token"
EOF
    
    # Create AppleScript to stop Jupyter Lab
    cat > "$SHORTCUTS_DIR/Stop Jupyter Lab.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/../../../JupyterLab"
docker compose down
EOF
    
    chmod +x "$SHORTCUTS_DIR"/*.command
    print_macos "Created desktop shortcuts in $SHORTCUTS_DIR"
fi

echo
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    print_success "🍎 macOS Docker Compose tests completed successfully!"
    echo -e "${GREEN}Your Jupyter Lab environment is optimized and ready for macOS!${NC}"
    
    # Offer to open Jupyter Lab
    read -p "Would you like to start Jupyter Lab now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_macos "Starting Jupyter Lab..."
        $COMPOSE_CMD up -d
        sleep 3
        print_success "Opening Jupyter Lab in your default browser..."
        open "http://localhost:8888/lab?token=datascience-token"
    fi
else
    print_error "⚠️ Test execution completed with failures on macOS."
    echo -e "${RED}Please review the macOS-specific issues above.${NC}"
fi

exit $TEST_EXIT_CODE