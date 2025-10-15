"""
Authorization Bypass Fix Validation Test Suite

Tests the security improvements for Issue #06 - Authorization Bypass in Data Processing
CWE-285: Improper Authorization

This test validates:
1. Session creation and management
2. Role-based access control (RBAC)
3. Permission-based function access
4. Authentication requirements
5. Authorization enforcement
6. Audit logging
"""

import sys
import os
from pathlib import Path
import io

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from data_processing import (
    create_session,
    get_session,
    revoke_session,
    clean_column_names,
    handle_missing_values,
    encode_categorical_variables,
    scale_features,
    detect_outliers,
    split_data,
    create_feature_summary,
    AuthenticationError,
    AuthorizationError,
    ROLES
)


# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore')

# Configure output for UTF-8 (Windows compatibility)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_test_header(message: str):
    """Print formatted test header."""
    print(f"\n{'='*60}")
    print(f"{message}")
    print(f"{'='*60}")


def print_test_result(test_name: str, passed: bool, details: str = ""):
    """Print formatted test result."""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {test_name}")
    if details:
        print(f"  Details: {details}")


def create_test_dataframe() -> pd.DataFrame:
    """Create a test DataFrame for testing."""
    return pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', None, 'Eve'],
        'Age': [25, 30, None, 40, 35],
        'Salary': [50000, 60000, 55000, 70000, 65000],
        'Department': ['IT', 'HR', 'IT', 'Finance', 'HR']
    })


def test_session_management():
    """Test 1: Session creation and management."""
    print_test_header("TEST 1: Session Management")
    
    all_passed = True
    
    # Test 1.1: Create valid session
    try:
        token = create_session('user1', 'admin')
        session = get_session(token)
        passed = session is not None and session['user_id'] == 'user1' and session['role'] == 'admin'
        print_test_result("Create valid admin session", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("Create valid admin session", False, str(e))
        all_passed = False
    
    # Test 1.2: Create data_scientist session
    try:
        token_ds = create_session('user2', 'data_scientist')
        session_ds = get_session(token_ds)
        passed = session_ds is not None and session_ds['role'] == 'data_scientist'
        print_test_result("Create data_scientist session", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("Create data_scientist session", False, str(e))
        all_passed = False
    
    # Test 1.3: Create viewer session
    try:
        token_viewer = create_session('user3', 'viewer')
        session_viewer = get_session(token_viewer)
        passed = session_viewer is not None and session_viewer['role'] == 'viewer'
        print_test_result("Create viewer session", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("Create viewer session", False, str(e))
        all_passed = False
    
    # Test 1.4: Reject invalid role
    try:
        token_invalid = create_session('user4', 'hacker')
        print_test_result("Reject invalid role", False, "Should have raised ValueError")
        all_passed = False
    except ValueError:
        print_test_result("Reject invalid role", True)
    except Exception as e:
        print_test_result("Reject invalid role", False, str(e))
        all_passed = False
    
    # Test 1.5: Revoke session
    try:
        test_token = create_session('user5', 'admin')
        revoked = revoke_session(test_token)
        session_after = get_session(test_token)
        passed = revoked and session_after is None
        print_test_result("Revoke session", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("Revoke session", False, str(e))
        all_passed = False
    
    # Test 1.6: Get non-existent session
    try:
        session_none = get_session('invalid_token')
        passed = session_none is None
        print_test_result("Get non-existent session returns None", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("Get non-existent session returns None", False, str(e))
        all_passed = False
    
    return all_passed


def test_role_permissions():
    """Test 2: Role-based permissions."""
    print_test_header("TEST 2: Role-Based Permissions")
    
    all_passed = True
    
    # Test 2.1: Admin has all permissions
    admin_perms = ROLES['admin']
    expected = ['read', 'write', 'delete', 'scale', 'encode', 'split', 'process']
    passed = all(perm in admin_perms for perm in expected)
    print_test_result("Admin has all permissions", passed, f"{len(admin_perms)} permissions")
    all_passed &= passed
    
    # Test 2.2: Data scientist permissions
    ds_perms = ROLES['data_scientist']
    expected_ds = ['read', 'write', 'scale', 'encode', 'split', 'process']
    passed = all(perm in ds_perms for perm in expected_ds) and 'delete' not in ds_perms
    print_test_result("Data scientist lacks delete permission", passed)
    all_passed &= passed
    
    # Test 2.3: Data analyst permissions
    da_perms = ROLES['data_analyst']
    expected_da = ['read', 'scale', 'encode', 'process']
    passed = all(perm in da_perms for perm in expected_da) and 'write' not in da_perms
    print_test_result("Data analyst lacks write permission", passed)
    all_passed &= passed
    
    # Test 2.4: Viewer has minimal permissions
    viewer_perms = ROLES['viewer']
    passed = viewer_perms == ['read']
    print_test_result("Viewer has only read permission", passed)
    all_passed &= passed
    
    return all_passed


def test_authentication_required():
    """Test 3: Authentication is required for all functions."""
    print_test_header("TEST 3: Authentication Required")
    
    all_passed = True
    df = create_test_dataframe()
    
    # Test 3.1: clean_column_names without token
    try:
        result = clean_column_names(df)
        print_test_result("clean_column_names rejects no token", False, "Should raise AuthenticationError")
        all_passed = False
    except AuthenticationError:
        print_test_result("clean_column_names rejects no token", True)
    except Exception as e:
        print_test_result("clean_column_names rejects no token", False, str(e))
        all_passed = False
    
    # Test 3.2: handle_missing_values without token
    try:
        result = handle_missing_values(df)
        print_test_result("handle_missing_values rejects no token", False, "Should raise AuthenticationError")
        all_passed = False
    except AuthenticationError:
        print_test_result("handle_missing_values rejects no token", True)
    except Exception as e:
        print_test_result("handle_missing_values rejects no token", False, str(e))
        all_passed = False
    
    # Test 3.3: encode_categorical_variables without token
    try:
        result, _ = encode_categorical_variables(df)
        print_test_result("encode_categorical_variables rejects no token", False, "Should raise AuthenticationError")
        all_passed = False
    except AuthenticationError:
        print_test_result("encode_categorical_variables rejects no token", True)
    except Exception as e:
        print_test_result("encode_categorical_variables rejects no token", False, str(e))
        all_passed = False
    
    # Test 3.4: scale_features without token
    try:
        result, _ = scale_features(df)
        print_test_result("scale_features rejects no token", False, "Should raise AuthenticationError")
        all_passed = False
    except AuthenticationError:
        print_test_result("scale_features rejects no token", True)
    except Exception as e:
        print_test_result("scale_features rejects no token", False, str(e))
        all_passed = False
    
    # Test 3.5: Invalid token
    try:
        result = clean_column_names(df, session_token='invalid_token_12345')
        print_test_result("Functions reject invalid token", False, "Should raise AuthenticationError")
        all_passed = False
    except AuthenticationError:
        print_test_result("Functions reject invalid token", True)
    except Exception as e:
        print_test_result("Functions reject invalid token", False, str(e))
        all_passed = False
    
    return all_passed


def test_authorization_enforcement():
    """Test 4: Authorization is properly enforced."""
    print_test_header("TEST 4: Authorization Enforcement")
    
    all_passed = True
    df = create_test_dataframe()
    
    # Create sessions for different roles
    admin_token = create_session('admin_user', 'admin')
    ds_token = create_session('ds_user', 'data_scientist')
    da_token = create_session('da_user', 'data_analyst')
    viewer_token = create_session('viewer_user', 'viewer')
    
    # Test 4.1: Admin can access all functions
    try:
        clean_column_names(df, session_token=admin_token)
        handle_missing_values(df, session_token=admin_token)
        scale_features(df[['Age', 'Salary']], session_token=admin_token)
        print_test_result("Admin can access all functions", True)
    except Exception as e:
        print_test_result("Admin can access all functions", False, str(e))
        all_passed = False
    
    # Test 4.2: Data scientist can process data
    try:
        clean_column_names(df, session_token=ds_token)
        handle_missing_values(df, session_token=ds_token)
        scale_features(df[['Age', 'Salary']], session_token=ds_token)
        print_test_result("Data scientist can process data", True)
    except Exception as e:
        print_test_result("Data scientist can process data", False, str(e))
        all_passed = False
    
    # Test 4.3: Data analyst can read and analyze
    try:
        clean_column_names(df, session_token=da_token)
        scale_features(df[['Age', 'Salary']], session_token=da_token)
        detect_outliers(df, session_token=da_token)
        print_test_result("Data analyst can read and analyze", True)
    except Exception as e:
        print_test_result("Data analyst can read and analyze", False, str(e))
        all_passed = False
    
    # Test 4.4: Viewer cannot modify data
    try:
        handle_missing_values(df, session_token=viewer_token)
        print_test_result("Viewer cannot modify data", False, "Should raise AuthorizationError")
        all_passed = False
    except AuthorizationError:
        print_test_result("Viewer cannot modify data", True)
    except Exception as e:
        print_test_result("Viewer cannot modify data", False, str(e))
        all_passed = False
    
    # Test 4.5: Viewer can only read
    try:
        clean_column_names(df, session_token=viewer_token)
        detect_outliers(df, session_token=viewer_token)
        create_feature_summary(df, session_token=viewer_token)
        print_test_result("Viewer can read data", True)
    except Exception as e:
        print_test_result("Viewer can read data", False, str(e))
        all_passed = False
    
    # Test 4.6: Data analyst cannot split data
    try:
        split_data(df, target_column='Age', session_token=da_token)
        print_test_result("Data analyst cannot split data", False, "Should raise AuthorizationError")
        all_passed = False
    except AuthorizationError:
        print_test_result("Data analyst cannot split data", True)
    except Exception as e:
        print_test_result("Data analyst cannot split data", False, str(e))
        all_passed = False
    
    return all_passed


def test_functional_integration():
    """Test 5: Functions work correctly with authorization."""
    print_test_header("TEST 5: Functional Integration")
    
    all_passed = True
    df = create_test_dataframe()
    
    # Create admin session for testing
    admin_token = create_session('functional_test_user', 'admin')
    
    # Test 5.1: clean_column_names works
    try:
        result = clean_column_names(df, session_token=admin_token)
        passed = 'name' in result.columns and 'age' in result.columns
        print_test_result("clean_column_names functions correctly", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("clean_column_names functions correctly", False, str(e))
        all_passed = False
    
    # Test 5.2: handle_missing_values works
    try:
        result = handle_missing_values(df, strategy='drop', session_token=admin_token)
        passed = result.isnull().sum().sum() < df.isnull().sum().sum()
        print_test_result("handle_missing_values functions correctly", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("handle_missing_values functions correctly", False, str(e))
        all_passed = False
    
    # Test 5.3: encode_categorical_variables works
    try:
        result, encoders = encode_categorical_variables(df, columns=['Department'], session_token=admin_token)
        passed = 'Department' in encoders and result['Department'].dtype in [np.int64, np.int32]
        print_test_result("encode_categorical_variables functions correctly", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("encode_categorical_variables functions correctly", False, str(e))
        all_passed = False
    
    # Test 5.4: scale_features works
    try:
        result, scaler = scale_features(df, columns=['Age', 'Salary'], session_token=admin_token)
        passed = scaler is not None and abs(result['Age'].mean()) < 1e-10
        print_test_result("scale_features functions correctly", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("scale_features functions correctly", False, str(e))
        all_passed = False
    
    # Test 5.5: detect_outliers works
    try:
        result = detect_outliers(df, columns=['Age', 'Salary'], session_token=admin_token)
        passed = 'Age_outlier' in result.columns and 'Salary_outlier' in result.columns
        print_test_result("detect_outliers functions correctly", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("detect_outliers functions correctly", False, str(e))
        all_passed = False
    
    # Test 5.6: create_feature_summary works
    try:
        result = create_feature_summary(df, session_token=admin_token)
        passed = 'column' in result.columns and len(result) == len(df.columns)
        print_test_result("create_feature_summary functions correctly", passed)
        all_passed &= passed
    except Exception as e:
        print_test_result("create_feature_summary functions correctly", False, str(e))
        all_passed = False
    
    return all_passed


def test_security_scenarios():
    """Test 6: Real-world security attack scenarios."""
    print_test_header("TEST 6: Security Attack Scenarios")
    
    all_passed = True
    df = create_test_dataframe()
    
    # Scenario 1: Attacker tries to bypass authentication
    try:
        result = handle_missing_values(df, session_token=None)
        print_test_result("Block unauthenticated access", False, "Should raise AuthenticationError")
        all_passed = False
    except AuthenticationError:
        print_test_result("Block unauthenticated access", True)
    except Exception as e:
        print_test_result("Block unauthenticated access", False, str(e))
        all_passed = False
    
    # Scenario 2: Privilege escalation attempt
    viewer_token = create_session('attacker', 'viewer')
    try:
        result = handle_missing_values(df, strategy='drop', session_token=viewer_token)
        print_test_result("Block privilege escalation", False, "Should raise AuthorizationError")
        all_passed = False
    except AuthorizationError:
        print_test_result("Block privilege escalation", True)
    except Exception as e:
        print_test_result("Block privilege escalation", False, str(e))
        all_passed = False
    
    # Scenario 3: Token hijacking (invalid token)
    try:
        fake_token = "session_hacker_123456789"
        result = clean_column_names(df, session_token=fake_token)
        print_test_result("Block token hijacking", False, "Should raise AuthenticationError")
        all_passed = False
    except AuthenticationError:
        print_test_result("Block token hijacking", True)
    except Exception as e:
        print_test_result("Block token hijacking", False, str(e))
        all_passed = False
    
    # Scenario 4: Session after revocation
    token = create_session('temp_user', 'admin')
    revoke_session(token)
    try:
        result = clean_column_names(df, session_token=token)
        print_test_result("Block revoked session", False, "Should raise AuthenticationError")
        all_passed = False
    except AuthenticationError:
        print_test_result("Block revoked session", True)
    except Exception as e:
        print_test_result("Block revoked session", False, str(e))
        all_passed = False
    
    # Scenario 5: Role manipulation (trying non-existent role)
    try:
        admin_token = create_session('fake_admin', 'superadmin')
        print_test_result("Block role manipulation", False, "Should raise ValueError")
        all_passed = False
    except ValueError:
        print_test_result("Block role manipulation", True)
    except Exception as e:
        print_test_result("Block role manipulation", False, str(e))
        all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("AUTHORIZATION BYPASS FIX VALIDATION TEST SUITE")
    print("Issue #06 - CWE-285: Improper Authorization")
    print("="*60)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Session Management", test_session_management()))
    test_results.append(("Role Permissions", test_role_permissions()))
    test_results.append(("Authentication Required", test_authentication_required()))
    test_results.append(("Authorization Enforcement", test_authorization_enforcement()))
    test_results.append(("Functional Integration", test_functional_integration()))
    test_results.append(("Security Attack Scenarios", test_security_scenarios()))
    
    # Print summary
    print_test_header("TEST SUMMARY")
    total_tests = len(test_results)
    passed_tests = sum(1 for _, passed in test_results if passed)
    
    for test_name, passed in test_results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("\n✅ ALL TESTS PASSED - Authorization bypass vulnerability is FIXED")
        print("✅ CWE-285: Improper Authorization - RESOLVED")
        return 0
    else:
        print(f"\n❌ {total_tests - passed_tests} TEST SUITE(S) FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
