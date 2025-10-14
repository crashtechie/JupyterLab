# Cross-Platform Docker Compose Jupyter Lab Testing Suite

## 📖 Overview

This comprehensive testing suite validates your Docker Compose Jupyter Lab environment across multiple operating systems with platform-specific optimizations and diagnostics.

## 🎯 Test Coverage

### System Requirements Validation
- ✅ Docker and Docker Compose installation
- ✅ Python environment setup and compatibility
- ✅ System resources (memory, disk space, CPU)
- ✅ Platform-specific prerequisites

### Docker Environment Testing
- ✅ Docker daemon status and accessibility
- ✅ Docker Compose configuration syntax validation
- ✅ Container networking and port availability
- ✅ Volume mounts and file permissions
- ✅ Service health checks and readiness probes

### Jupyter Lab Integration Testing
- ✅ Container startup and initialization
- ✅ Web interface accessibility (http://localhost:8888)
- ✅ Authentication token validation
- ✅ Scientific package availability (pandas, numpy, matplotlib, etc.)
- ✅ File system operations and notebook creation
- ✅ Python kernel functionality

## 🖥️ Platform Support

### Windows (PowerShell)
**Script**: `run_tests.ps1`

**Features**:
- Native PowerShell 5.1+ and 7.x support
- Windows Subsystem for Linux (WSL) detection
- Docker Desktop integration checks
- Windows-specific path handling
- Registry and system service validation
- Hyper-V and WSL2 backend detection

**Optimizations**:
- Windows container mode detection
- Performance monitoring with native tools
- Windows Defender exclusion recommendations
- PowerShell execution policy handling

### Linux (Distribution-Aware)
**Script**: `run_tests_linux.sh`

**Features**:
- Automatic distribution detection (Ubuntu, Debian, Fedora, CentOS, Arch, etc.)
- Package manager integration (apt, dnf, yum, pacman, zypper)
- Systemd service management
- SELinux and AppArmor compatibility
- cgroups v1/v2 detection
- Firewall configuration checks

**Optimizations**:
- Distribution-specific package installation
- systemd user service creation
- Desktop environment integration
- Container runtime optimization
- Resource limit configuration

### macOS (Apple Silicon Ready)
**Script**: `run_tests_macos.sh`

**Features**:
- Apple Silicon (M1/M2/M3) and Intel detection
- Homebrew package manager integration
- Docker Desktop for Mac validation
- macOS version compatibility checks
- Xcode Command Line Tools detection
- Container architecture verification

**Optimizations**:
- Native ARM64 container preference
- Rosetta 2 emulation detection
- macOS-specific performance tuning
- Spotlight indexing exclusions
- Battery optimization recommendations

### Universal Unix/Linux
**Script**: `run_tests.sh`

**Features**:
- POSIX-compliant shell scripting
- Cross-platform command detection
- Generic Unix system validation
- Fallback compatibility mode
- Basic Docker functionality testing

## 🔧 Platform-Specific Diagnostics

### Windows Diagnostics
```powershell
# Check Docker Desktop status
Get-Process "Docker Desktop" -ErrorAction SilentlyContinue

# Validate WSL integration
wsl --list --verbose

# Check Hyper-V features
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V

# Network connectivity test
Test-NetConnection localhost -Port 8888
```

### Linux Diagnostics
```bash
# Check Docker service status
systemctl status docker

# Validate container runtime
docker info --format '{{.DefaultRuntime}}'

# Check SELinux context
ls -Z /var/lib/docker

# Memory and cgroups
cat /proc/meminfo
ls /sys/fs/cgroup/
```

### macOS Diagnostics
```bash
# Check Docker Desktop
osascript -e 'tell application "System Events" to get name of processes' | grep -i docker

# Validate architecture support
docker version --format '{{.Server.Arch}}'

# Check file sharing permissions
docker run --rm -v "$PWD:/test" alpine ls -la /test
```

## 📊 Test Results and Reporting

### Output Formats
- **Console Output**: Real-time colored progress indicators
- **JSON Reports**: Structured results in `scripts/tests/results/`
- **System Information**: Detailed platform diagnostics
- **Error Logs**: Comprehensive failure analysis

### Report Files Generated
```
scripts/tests/results/
├── test_results.json      # Main test results
├── system_info.json       # Platform information
├── docker_info.json       # Docker configuration
├── performance_metrics.json # Resource usage
└── platform_diagnostics.json # OS-specific details
```

### Integration with CI/CD
The test scripts are designed to work in automated environments:

```yaml
# GitHub Actions example
- name: Run Docker Compose Tests
  run: |
    chmod +x scripts/tests/run_tests.sh
    ./scripts/tests/run_tests.sh
  
# GitLab CI example  
test:docker:
  script:
    - ./scripts/tests/run_tests_linux.sh
    
# Azure DevOps example
- script: |
    .\scripts\tests\run_tests.ps1
  displayName: 'Docker Compose Validation'
```

## 🚀 Usage Examples

### Quick Validation
```bash
# Any platform - automatic detection
cd JupyterLab

# Windows
.\scripts\tests\run_tests.ps1

# Linux/macOS  
./scripts/tests/run_tests.sh
```

### Advanced Platform Testing
```bash
# Linux with distribution-specific optimizations
./scripts/tests/run_tests_linux.sh

# macOS with Apple Silicon optimizations
./scripts/tests/run_tests_macos.sh

# Verbose Windows testing
.\scripts\tests\run_tests.ps1 -Verbose
```

### Continuous Integration
```bash
# Non-interactive mode
./scripts/tests/run_tests.sh --ci-mode

# JSON output only
./scripts/tests/run_tests.sh --json-only

# Skip interactive prompts
./scripts/tests/run_tests.sh --no-prompt
```

## 🔍 Troubleshooting Guide

### Common Platform Issues

#### Windows
- **Docker Desktop not starting**: Check Hyper-V/WSL2 backend
- **Port conflicts**: Windows services using port 8888
- **File permissions**: NTFS vs WSL2 file system differences
- **Network isolation**: Windows Firewall blocking Docker

#### Linux
- **Docker daemon issues**: Service not running or user permissions
- **SELinux/AppArmor**: Security policies blocking container operations
- **systemd integration**: User vs system service configurations
- **Distribution packages**: Missing Docker Compose or outdated versions

#### macOS
- **Docker Desktop resources**: Insufficient memory/CPU allocation
- **File sharing**: macOS privacy settings blocking directory access
- **Architecture mismatch**: Intel vs ARM64 container images
- **Network restrictions**: Corporate firewall or VPN interference

### Debugging Steps

1. **Run Diagnostics**: Use appropriate platform test script
2. **Check Dependencies**: Verify Docker and Docker Compose versions
3. **Validate Configuration**: Review docker-compose.yml syntax
4. **Test Network**: Ensure port 8888 is available
5. **Review Logs**: Check container and system logs
6. **Platform Specifics**: Follow platform-specific troubleshooting

## 🌟 Features and Benefits

### Automated Detection
- Operating system and version identification
- Architecture detection (x86_64, ARM64, etc.)
- Package manager and dependency resolution
- Container runtime and orchestration validation

### Comprehensive Testing
- End-to-end workflow validation
- Performance benchmarking
- Security configuration checks
- Integration testing with external services

### Developer Experience
- Colored console output with progress indicators
- Detailed error messages with resolution suggestions
- Platform-specific optimization recommendations
- Integration with popular development tools

### Production Readiness
- CI/CD pipeline integration
- Non-interactive execution modes
- Structured JSON reporting
- Comprehensive logging and auditing

## 📚 Additional Resources

### Platform-Specific Documentation
- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/)
- **Linux**: [Docker Engine Installation](https://docs.docker.com/engine/install/)
- **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/)

### Testing Frameworks
- **PowerShell**: [Pester Testing Framework](https://pester.dev/)
- **Bash**: [Bash Automated Testing System](https://github.com/bats-core/bats-core)
- **Python**: [pytest for Docker](https://pytest-docker.readthedocs.io/)

### Container Orchestration
- **Docker Compose**: [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- **Kubernetes**: [Local Development](https://kubernetes.io/docs/tasks/tools/)
- **Podman**: [Docker Compatibility](https://podman.io/getting-started/)

---

**Created**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss UTC")
**Platform**: Cross-Platform (Windows, Linux, macOS)
**Version**: 1.0.0
**Maintained By**: Jupyter Lab Docker Compose Project