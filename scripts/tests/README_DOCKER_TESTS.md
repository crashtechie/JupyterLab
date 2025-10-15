# Docker Security Testing

This directory contains comprehensive security validation tests for Issues #01-#05, designed to run in the Docker container environment to ensure production readiness.

## Test Files

### Main Test Suites
- **`test_docker_security_fixes.py`** - Comprehensive test covering all 5 resolved security issues
- **`test_path_traversal_fix.py`** - Detailed tests for Issue #04 (CWE-22 Path Traversal)
- **`test_command_injection_fix.py`** - Detailed tests for Issue #05 (CWE-77,78,88 Command Injection)

### Test Runners
- **`run_docker_tests.sh`** - Bash script to run all tests in Docker (Linux/Mac/Git Bash)
- **`run_docker_tests.ps1`** - PowerShell script to run all tests in Docker (Windows)

### Configuration
- **`docker-compose.test.yml`** - Docker Compose override for test environment

## Quick Start

### Option 1: Automated Test Runner (Recommended)

**Windows (PowerShell):**
```powershell
.\scripts\tests\run_docker_tests.ps1
```

**Linux/Mac/Git Bash:**
```bash
chmod +x scripts/tests/run_docker_tests.sh
./scripts/tests/run_docker_tests.sh
```

This will:
1. Start the Docker test environment
2. Run all security tests inside the container
3. Display results for each issue
4. Optionally keep containers running for manual testing

### Option 2: Manual Testing

**1. Start the test environment:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d
```

**2. Run comprehensive security tests:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml exec jupyter \
  python /home/jovyan/work/scripts/tests/test_docker_security_fixes.py
```

**3. Run individual test suites:**
```bash
# Path Traversal Tests (Issue #04)
docker-compose -f docker-compose.yml -f docker-compose.test.yml exec jupyter \
  python /home/jovyan/work/scripts/tests/test_path_traversal_fix.py

# Command Injection Tests (Issue #05)
docker-compose -f docker-compose.yml -f docker-compose.test.yml exec jupyter \
  python /home/jovyan/work/scripts/tests/test_command_injection_fix.py
```

**4. Stop the test environment:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml down
```

### Option 3: Interactive Container Testing

Enter the container for manual testing:
```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d
docker exec -it jupyterlab-datascience bash

# Inside container:
cd /home/jovyan/work
python scripts/tests/test_docker_security_fixes.py
```

## What Gets Tested

### Issue #01: Critical - Insecure Cryptography (CWE-327)
- ✅ Verifies urllib3 >= 2.0.0
- ✅ Verifies cryptography >= 40.0.0
- ✅ Confirms secure SSL/TLS implementation

### Issue #02: High - Sensitive Information Leak - Token Generator (CWE-200)
- ✅ Verifies no token printing/logging in generation scripts
- ✅ Confirms 384-bit security implementation
- ✅ Validates secure storage methods

### Issue #03: High - Sensitive Information Leak - Postgres Password (CWE-200)
- ✅ Verifies no password printing/logging in generation scripts
- ✅ Confirms secure password handling
- ✅ Validates proper storage practices

### Issue #04: High - Path Traversal Vulnerability (CWE-22)
- ✅ Tests normal file path operations work correctly
- ✅ Blocks path traversal attacks (../../../etc/passwd)
- ✅ Rejects invalid directory types
- ✅ Validates allowlist enforcement
- ✅ Tests 5+ attack vectors

### Issue #05: High - OS Command Injection (CWE-77,78,88)
- ✅ Validates safe subprocess execution
- ✅ Blocks command injection attempts (;, |, &&, etc.)
- ✅ Enforces argument list usage (no shell=True)
- ✅ Tests input validation and sanitization
- ✅ Validates timeout protection
- ✅ Tests 7+ attack vectors

## Expected Output

### Successful Test Run
```
=======================================================================
DOCKER CONTAINER SECURITY VALIDATION
Comprehensive Test Suite for Issues #01-#05
=======================================================================

ENVIRONMENT CHECK
=======================================================================
Platform: linux
Python: 3.x.x
Working Directory: /home/jovyan/work
Running in Docker: Yes
✓ Docker container environment detected

=======================================================================
ISSUE #01: Critical - Insecure Cryptography (CWE-327)
=======================================================================
urllib3 version: 2.x.x
cryptography version: 4x.x.x
✓ PASS: Secure versions installed
✓ CWE-327: Insecure cryptography vulnerability RESOLVED

[... more tests ...]

=======================================================================
FINAL RESULTS
=======================================================================
✓ PASS: Issue #01: Insecure Cryptography
✓ PASS: Issue #02: Token Leak
✓ PASS: Issue #03: Password Leak
✓ PASS: Issue #04: Path Traversal
✓ PASS: Issue #05: Command Injection
=======================================================================
Results: 5/5 tests passed

✅ ALL SECURITY FIXES VALIDATED
✅ Production environment (Docker) is secure
=======================================================================
```

## CI/CD Integration

Add to your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
test-security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Run Docker Security Tests
      run: |
        chmod +x scripts/tests/run_docker_tests.sh
        ./scripts/tests/run_docker_tests.sh
```

## Troubleshooting

### Container won't start
```bash
# Check Docker logs
docker-compose -f docker-compose.yml -f docker-compose.test.yml logs

# Rebuild containers
docker-compose -f docker-compose.yml -f docker-compose.test.yml build --no-cache
```

### Tests fail in container but pass locally
This is expected! The tests are designed to verify fixes work in the production Linux environment. Local Windows tests validate development environment only.

### Import errors
Ensure the PYTHONPATH is set correctly in docker-compose.test.yml:
```yaml
environment:
  - PYTHONPATH=/home/jovyan/work/scripts
```

## Maintenance

When adding new security fixes:
1. Add test function to `test_docker_security_fixes.py`
2. Update this README with the new issue
3. Update the test summary output
4. Run full test suite to ensure no regressions

## Notes

- Tests are designed to be idempotent (can run multiple times)
- No modifications are made to the container filesystem
- Tests validate security posture, not functionality
- Some tests may show platform-specific variations (acceptable)
