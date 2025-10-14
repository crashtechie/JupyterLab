#!/bin/bash
# Docker Compose Jupyter Lab Test Runner - Linux Optimized
# This script runs end-to-end tests with Linux-specific optimizations

set -e  # Exit on any error

# Colors for output
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

echo -e "${CYAN}🐧 Docker Compose Jupyter Lab Tests - Linux Edition${NC}"
echo -e "${CYAN}===================================================${NC}"

# Change to project root
cd "$PROJECT_ROOT"

# Function to print status messages
print_status() {
    echo -e "${BLUE}ℹ️  [INFO]${NC} $1"
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

print_linux() {
    echo -e "${PURPLE}🐧 [LINUX]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect Linux distribution
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        DISTRO="$ID"
        VERSION="$VERSION_ID"
        DISTRO_NAME="$PRETTY_NAME"
    elif command_exists lsb_release; then
        DISTRO=$(lsb_release -si | tr '[:upper:]' '[:lower:]')
        VERSION=$(lsb_release -sr)
        DISTRO_NAME=$(lsb_release -sd)
    elif [[ -f /etc/redhat-release ]]; then
        DISTRO="rhel"
        DISTRO_NAME=$(cat /etc/redhat-release)
    elif [[ -f /etc/debian_version ]]; then
        DISTRO="debian"
        DISTRO_NAME="Debian $(cat /etc/debian_version)"
    else
        DISTRO="unknown"
        DISTRO_NAME="Unknown Linux"
    fi
}

# System Information
print_linux "Gathering Linux system information..."
detect_distro

KERNEL_VERSION=$(uname -r)
ARCH=$(uname -m)
HOSTNAME=$(hostname)

print_success "Distribution: $DISTRO_NAME"
print_success "Kernel: $KERNEL_VERSION"
print_success "Architecture: $ARCH"
print_success "Hostname: $HOSTNAME"

# Detect package manager and set commands
case "$DISTRO" in
    ubuntu|debian|mint|pop)
        PKG_MANAGER="apt"
        PKG_INSTALL="sudo apt update && sudo apt install -y"
        PKG_SEARCH="apt search"
        PYTHON_PKG="python3 python3-pip python3-venv"
        ;;
    fedora)
        PKG_MANAGER="dnf"
        PKG_INSTALL="sudo dnf install -y"
        PKG_SEARCH="dnf search"
        PYTHON_PKG="python3 python3-pip python3-virtualenv"
        ;;
    centos|rhel|rocky|almalinux)
        PKG_MANAGER="yum"
        PKG_INSTALL="sudo yum install -y"
        PKG_SEARCH="yum search"
        PYTHON_PKG="python3 python3-pip"
        ;;
    arch|manjaro|endeavouros)
        PKG_MANAGER="pacman"
        PKG_INSTALL="sudo pacman -S --noconfirm"
        PKG_SEARCH="pacman -Ss"
        PYTHON_PKG="python python-pip"
        ;;
    opensuse*|suse)
        PKG_MANAGER="zypper"
        PKG_INSTALL="sudo zypper install -y"
        PKG_SEARCH="zypper search"
        PYTHON_PKG="python3 python3-pip python3-virtualenv"
        ;;
    *)
        PKG_MANAGER="unknown"
        print_warning "Unknown Linux distribution. Manual package installation may be required."
        ;;
esac

print_linux "Package Manager: $PKG_MANAGER"

# Check system resources
print_linux "Checking system resources..."

# Memory check
if command_exists free; then
    MEMORY_INFO=$(free -h | grep "^Mem:" | awk '{print $2 " total, " $3 " used, " $7 " available"}')
    print_linux "Memory: $MEMORY_INFO"
    
    # Check if sufficient memory is available
    AVAILABLE_MB=$(free -m | grep "^Mem:" | awk '{print $7}')
    if [[ "$AVAILABLE_MB" -lt 2048 ]]; then
        print_warning "Less than 2GB memory available. Docker containers may run slowly."
    fi
fi

# Disk space check
DISK_INFO=$(df -h / | tail -1 | awk '{print $4 " available on " $6}')
print_linux "Disk Space: $DISK_INFO"

# Check if running in WSL
if grep -qi microsoft /proc/version 2>/dev/null; then
    print_linux "WSL (Windows Subsystem for Linux) detected"
    WSL_DETECTED=true
    
    # WSL-specific checks
    if command_exists wslpath 2>/dev/null; then
        WINDOWS_USER=$(cmd.exe /C "echo %USERNAME%" 2>/dev/null | tr -d '\r\n' || echo "unknown")
        print_linux "Windows User: $WINDOWS_USER"
    fi
else
    WSL_DETECTED=false
fi

# Check prerequisites
print_status "Checking prerequisites..."

# Check Docker installation
if ! command_exists docker; then
    print_error "Docker is not installed."
    print_linux "Install Docker with:"
    
    case "$PKG_MANAGER" in
        apt)
            echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
            echo "  sudo sh get-docker.sh"
            echo "  sudo usermod -aG docker \$USER"
            ;;
        dnf|yum)
            echo "  $PKG_INSTALL docker"
            echo "  sudo systemctl enable --now docker"
            echo "  sudo usermod -aG docker \$USER"
            ;;
        pacman)
            echo "  $PKG_INSTALL docker docker-compose"
            echo "  sudo systemctl enable --now docker"
            echo "  sudo usermod -aG docker \$USER"
            ;;
        *)
            echo "  Visit: https://docs.docker.com/engine/install/"
            ;;
    esac
    exit 1
fi

# Check if Docker daemon is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker daemon is not running."
    
    if [[ "$WSL_DETECTED" == "true" ]]; then
        print_linux "In WSL, start Docker Desktop on Windows or install Docker directly in WSL"
    else
        print_linux "Start Docker with: sudo systemctl start docker"
    fi
    exit 1
fi

DOCKER_VERSION=$(docker --version)
print_success "Docker: $DOCKER_VERSION"

# Check Docker Compose
if docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command_exists docker-compose; then
    COMPOSE_CMD="docker-compose"
    print_warning "Using legacy docker-compose. Consider upgrading to Docker Compose V2"
else
    print_error "Docker Compose is not available."
    print_linux "Install with:"
    case "$PKG_MANAGER" in
        apt)
            echo "  sudo apt install docker-compose-plugin"
            ;;
        dnf|yum)
            echo "  sudo dnf install docker-compose-plugin"
            ;;
        pacman)
            echo "  sudo pacman -S docker-compose"
            ;;
        *)
            echo "  Visit: https://docs.docker.com/compose/install/"
            ;;
    esac
    exit 1
fi

COMPOSE_VERSION=$($COMPOSE_CMD version)
print_success "Docker Compose: $COMPOSE_VERSION"

# Check Python
PYTHON_CMD=""
for py_cmd in python3.12 python3.11 python3.10 python3.9 python3 python; do
    if command_exists "$py_cmd"; then
        PYTHON_CMD="$py_cmd"
        break
    fi
done

if [[ -z "$PYTHON_CMD" ]]; then
    print_error "Python is not installed."
    print_linux "Install Python with: $PKG_INSTALL $PYTHON_PKG"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
print_success "Python: $PYTHON_VERSION"

# Check pip
PIP_CMD=""
for pip_cmd in pip3 pip; do
    if command_exists "$pip_cmd"; then
        PIP_CMD="$pip_cmd"
        break
    fi
done

if [[ -z "$PIP_CMD" ]]; then
    print_warning "pip not found. Attempting to install..."
    
    case "$PKG_MANAGER" in
        apt)
            sudo apt update && sudo apt install -y python3-pip
            ;;
        dnf|yum)
            sudo $PKG_MANAGER install -y python3-pip
            ;;
        pacman)
            sudo pacman -S --noconfirm python-pip
            ;;
        *)
            print_error "Please install pip manually"
            exit 1
            ;;
    esac
    
    PIP_CMD="pip3"
fi

# Linux-specific Docker optimizations
print_linux "Applying Linux-specific Docker optimizations..."

# Check if user is in docker group
if ! groups "$USER" | grep -q docker; then
    print_warning "User '$USER' is not in the docker group."
    print_warning "Add with: sudo usermod -aG docker $USER"
    print_warning "Then log out and back in, or use: newgrp docker"
    
    # Try to use newgrp if available
    if command_exists newgrp; then
        print_linux "Attempting to use newgrp docker for this session..."
        exec newgrp docker "$0" "$@"
    fi
fi

# Check cgroup version (affects Docker performance)
if [[ -f /sys/fs/cgroup/cgroup.controllers ]]; then
    print_linux "Using cgroups v2 (systemd)"
elif [[ -d /sys/fs/cgroup/memory ]]; then
    print_linux "Using cgroups v1"
else
    print_warning "Cannot determine cgroup version"
fi

# Set resource limits if running as root or in container
if [[ "$EUID" -eq 0 ]] || [[ -f /.dockerenv ]]; then
    print_linux "Running as root or in container - setting resource limits"
    ulimit -n 65536 2>/dev/null || true
fi

# Install required Python packages
print_status "Installing required Python packages..."

# Create requirements for Linux
TEMP_REQ_FILE="/tmp/linux_requirements_$$.txt"
cat > "$TEMP_REQ_FILE" << EOF
requests>=2.25.0
urllib3>=1.26.0
certifi>=2021.5.25
psutil>=5.8.0
EOF

# Install with user flag if not root
if [[ "$EUID" -ne 0 ]]; then
    $PIP_CMD install --user -r "$TEMP_REQ_FILE"
else
    $PIP_CMD install -r "$TEMP_REQ_FILE"
fi

print_success "Python packages installed successfully"
rm -f "$TEMP_REQ_FILE"

# Linux-specific system checks
print_linux "Performing Linux-specific checks..."

# Check systemd (if available)
if command_exists systemctl; then
    DOCKER_STATUS=$(systemctl is-active docker 2>/dev/null || echo "unknown")
    print_linux "Docker service status: $DOCKER_STATUS"
    
    if [[ "$DOCKER_STATUS" != "active" ]] && [[ "$WSL_DETECTED" == "false" ]]; then
        print_warning "Docker service is not active. Start with: sudo systemctl start docker"
    fi
fi

# Check SELinux (if available)
if command_exists getenforce; then
    SELINUX_STATUS=$(getenforce 2>/dev/null || echo "disabled")
    print_linux "SELinux status: $SELINUX_STATUS"
    
    if [[ "$SELINUX_STATUS" == "Enforcing" ]]; then
        print_warning "SELinux is enforcing. Docker volumes may need proper context."
        print_warning "Consider: sudo setsebool -P container_manage_cgroup on"
    fi
fi

# Check firewall status
if command_exists ufw; then
    UFW_STATUS=$(sudo ufw status 2>/dev/null | head -1 || echo "unknown")
    print_linux "UFW firewall: $UFW_STATUS"
elif command_exists firewall-cmd; then
    FIREWALL_STATUS=$(sudo firewall-cmd --state 2>/dev/null || echo "unknown")
    print_linux "FirewallD: $FIREWALL_STATUS"
fi

# Set Linux-specific environment variables
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Optimize for specific distributions
case "$DISTRO" in
    ubuntu|debian)
        # Ubuntu/Debian optimizations
        export DEBIAN_FRONTEND=noninteractive
        ;;
    fedora|centos|rhel)
        # Red Hat family optimizations
        export LANG=C.UTF-8
        ;;
    arch)
        # Arch Linux optimizations
        export LANG=en_US.UTF-8
        ;;
esac

print_linux "Applied Linux distribution-specific optimizations"

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

# Check results and provide Linux-specific feedback
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    print_success "All tests passed successfully! 🎉"
    print_success "Your Docker Compose Jupyter Lab setup is working correctly on Linux."
    
    echo
    print_linux "Linux-optimized commands:"
    echo "  • Start Jupyter Lab: $COMPOSE_CMD up -d"
    echo "  • Access at: http://localhost:8888"
    echo "  • Token: datascience-token"
    echo "  • Stop services: $COMPOSE_CMD down"
    echo "  • View logs: $COMPOSE_CMD logs -f jupyter"
    echo "  • System logs: journalctl -u docker"
    
else
    print_error "Some tests failed. ❌"
    print_error "Check the results in scripts/tests/results/"
    
    echo
    print_linux "Linux troubleshooting:"
    echo "  • Restart Docker: sudo systemctl restart docker"
    echo "  • Check Docker logs: journalctl -u docker"
    echo "  • View container logs: docker logs <container_name>"
    echo "  • Check permissions: ls -la /var/run/docker.sock"
    
    case "$DISTRO" in
        ubuntu|debian)
            echo "  • Ubuntu/Debian: Check AppArmor profiles"
            ;;
        fedora|centos|rhel)
            echo "  • RHEL family: Check SELinux contexts"
            ;;
        arch)
            echo "  • Arch: Check systemd user services"
            ;;
    esac
fi

# Create Linux-specific service files
print_linux "Creating Linux integration files..."

# Create systemd user service (if systemd is available)
if command_exists systemctl && [[ "$EUID" -ne 0 ]]; then
    USER_SERVICE_DIR="$HOME/.config/systemd/user"
    mkdir -p "$USER_SERVICE_DIR"
    
    cat > "$USER_SERVICE_DIR/jupyter-lab.service" << EOF
[Unit]
Description=Jupyter Lab Docker Compose
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_ROOT
ExecStart=$COMPOSE_CMD up -d
ExecStop=$COMPOSE_CMD down
TimeoutStartSec=0

[Install]
WantedBy=default.target
EOF
    
    systemctl --user daemon-reload
    print_linux "Created systemd user service: jupyter-lab.service"
    print_linux "Enable with: systemctl --user enable jupyter-lab.service"
fi

# Create desktop entry
if [[ -d "$HOME/.local/share/applications" ]]; then
    cat > "$HOME/.local/share/applications/jupyter-lab.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Jupyter Lab (Docker)
Comment=Data Science Environment
Exec=bash -c "cd '$PROJECT_ROOT' && $COMPOSE_CMD up -d && sleep 3 && xdg-open 'http://localhost:8888/lab?token=datascience-token'"
Icon=applications-science
Terminal=false
Categories=Development;Science;
EOF
    
    print_linux "Created desktop entry: jupyter-lab.desktop"
fi

echo
print_linux "Linux system information:"
echo "  • Distribution: $DISTRO_NAME"
echo "  • Package Manager: $PKG_MANAGER"
echo "  • Init System: $(ps -p 1 -o comm= 2>/dev/null || echo 'unknown')"
echo "  • Container Runtime: $(docker info --format '{{.DefaultRuntime}}' 2>/dev/null || echo 'unknown')"

if [[ "$WSL_DETECTED" == "true" ]]; then
    echo "  • WSL Environment: Use Docker Desktop or native Docker"
    echo "  • Windows Integration: Available via WSL2"
fi

echo
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
    print_success "🐧 Linux Docker Compose tests completed successfully!"
    echo -e "${GREEN}Your Jupyter Lab environment is optimized and ready for Linux!${NC}"
    
    # Offer to start Jupyter Lab
    read -p "Would you like to start Jupyter Lab now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_linux "Starting Jupyter Lab..."
        $COMPOSE_CMD up -d
        sleep 3
        print_success "Jupyter Lab started! Access at: http://localhost:8888"
        
        # Try to open in browser if GUI is available
        if [[ -n "$DISPLAY" ]] && command_exists xdg-open; then
            print_linux "Opening in browser..."
            xdg-open "http://localhost:8888/lab?token=datascience-token" &
        fi
    fi
else
    print_error "⚠️ Test execution completed with failures on Linux."
    echo -e "${RED}Please review the Linux-specific issues above.${NC}"
fi

exit $TEST_EXIT_CODE