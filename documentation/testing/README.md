# Testing Documentation

This section contains testing documentation for the JupyterLab project, including test procedures, cross-platform testing guides, and security validation tests.

## 📁 Available Documentation

### 🔒 [Docker Security Testing](docker-security-testing.md)
Comprehensive security validation tests for all resolved security issues, designed to run in the Docker container environment.

**Contents:**
- Security test suites for Issues #01-#05
- Path traversal vulnerability tests
- Command injection prevention tests
- Automated test runners for Windows, Linux, and macOS
- Docker Compose test configuration

### 🌐 [Cross-Platform Testing](cross-platform-testing.md)
Guidelines and procedures for testing the JupyterLab environment across Windows, Linux, and macOS platforms.

**Contents:**
- Platform-specific test procedures
- Compatibility verification steps
- Environment setup for each platform
- Troubleshooting common platform-specific issues

## 🚀 Quick Start

### Run All Security Tests

**Windows (PowerShell):**
```powershell
.\scripts\tests\run_docker_tests.ps1
```

**Linux/Mac:**
```bash
./scripts/tests/run_docker_tests.sh
```

### Run Specific Test Suites

**All comprehensive tests:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml exec jupyter \
  python /home/jovyan/work/scripts/tests/test_docker_security_fixes.py
```

**Platform-specific tests:**
- Windows: `.\scripts\tests\run_tests.ps1`
- Linux: `./scripts/tests/run_tests_linux.sh`
- macOS: `./scripts/tests/run_tests_macos.sh`

## 📋 Test Categories

### Security Tests
- Cryptography validation (384-bit security)
- Path traversal prevention
- Command injection protection
- Authorization checks
- Token security validation

### Integration Tests
- Docker environment setup
- PostgreSQL connection and security
- Jupyter Lab authentication
- Cross-platform compatibility

### Unit Tests
- Utility function validation
- Data processing scripts
- Token generation/recovery

## 📖 Related Documentation

- [Security Documentation](../security/) - Security issues and reviews
- [Development Setup](../development/Development-Setup.md) - Developer environment setup
- [Security Best Practices](../development/Security-Best-Practices.md) - Security guidelines

## 🔧 Test Infrastructure

### Docker Test Environment
- `docker-compose.test.yml` - Test-specific Docker configuration
- Isolated test containers
- Automated cleanup procedures

### Test Scripts Location
All test scripts are located in `scripts/tests/`:
- Python test files (`test_*.py`)
- Platform-specific runners (`run_tests.ps1`, `run_tests.sh`, etc.)
- Validation scripts (`validate_*.py`)

## 💡 Best Practices

1. **Always run security tests** before committing changes to security-sensitive code
2. **Test on all platforms** when making cross-platform changes
3. **Review test results** carefully and address all failures
4. **Keep tests updated** when adding new features or fixing bugs
5. **Document test procedures** for new functionality
