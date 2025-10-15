"""
Test script to validate path traversal vulnerability fixes in utils.py
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import get_data_path, get_output_path, get_project_root

def test_normal_usage():
    """Test normal, legitimate usage"""
    print("=" * 60)
    print("TEST 1: Normal Usage")
    print("=" * 60)
    
    try:
        # Test normal data path
        path = get_data_path("test.csv", "raw")
        print(f"✓ Normal data path: {path}")
        assert str(get_project_root() / "data" / "raw") in str(path)
        
        # Test normal output path
        path = get_output_path("plot.png", "figures")
        print(f"✓ Normal output path: {path}")
        assert str(get_project_root() / "outputs" / "figures") in str(path)
        
        print("✓ Normal usage tests PASSED\n")
        return True
    except Exception as e:
        print(f"✗ Normal usage tests FAILED: {e}\n")
        return False

def test_path_traversal_attempts():
    """Test that path traversal attempts are blocked"""
    print("=" * 60)
    print("TEST 2: Path Traversal Attack Prevention")
    print("=" * 60)
    
    test_cases = [
        ("../../../etc/passwd", "raw"),
        ("../../secrets.txt", "processed"),
        ("..\\..\\..\\Windows\\System32\\config\\SAM", "raw"),
        ("../../../database/init/01-init.sql", "external"),
        ("./../../../README.md", "raw"),
    ]
    
    passed = 0
    failed = 0
    
    for filename, data_type in test_cases:
        try:
            path = get_data_path(filename, data_type)
            print(f"✗ FAILED to block: {filename}")
            print(f"  Returned path: {path}")
            failed += 1
        except ValueError as e:
            print(f"✓ Blocked path traversal: {filename}")
            print(f"  Error: {e}")
            passed += 1
        except Exception as e:
            print(f"? Unexpected error for {filename}: {e}")
            failed += 1
    
    print(f"\nPath Traversal Prevention: {passed} passed, {failed} failed\n")
    return failed == 0

def test_output_path_traversal():
    """Test output path traversal prevention"""
    print("=" * 60)
    print("TEST 3: Output Path Traversal Prevention")
    print("=" * 60)
    
    test_cases = [
        ("../../../etc/passwd", "figures"),
        ("../../config.json", "models"),
        ("..\\..\\..\\sensitive_data.txt", "reports"),
    ]
    
    passed = 0
    failed = 0
    
    for filename, output_type in test_cases:
        try:
            path = get_output_path(filename, output_type)
            print(f"✗ FAILED to block: {filename}")
            print(f"  Returned path: {path}")
            failed += 1
        except ValueError as e:
            print(f"✓ Blocked path traversal: {filename}")
            print(f"  Error: {e}")
            passed += 1
        except Exception as e:
            print(f"? Unexpected error for {filename}: {e}")
            failed += 1
    
    print(f"\nOutput Path Prevention: {passed} passed, {failed} failed\n")
    return failed == 0

def test_invalid_directory_types():
    """Test that invalid directory types are rejected"""
    print("=" * 60)
    print("TEST 4: Invalid Directory Type Validation")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test invalid data_type
    try:
        path = get_data_path("test.csv", "invalid_type")
        print(f"✗ FAILED to reject invalid data_type")
        failed += 1
    except ValueError as e:
        print(f"✓ Rejected invalid data_type: {e}")
        passed += 1
    
    # Test invalid output_type
    try:
        path = get_output_path("test.png", "invalid_type")
        print(f"✗ FAILED to reject invalid output_type")
        failed += 1
    except ValueError as e:
        print(f"✓ Rejected invalid output_type: {e}")
        passed += 1
    
    print(f"\nDirectory Type Validation: {passed} passed, {failed} failed\n")
    return failed == 0

def test_subdirectories():
    """Test that legitimate subdirectories work"""
    print("=" * 60)
    print("TEST 5: Legitimate Subdirectory Usage")
    print("=" * 60)
    
    try:
        # Test subdirectory in data path
        path = get_data_path("subdir/test.csv", "raw")
        print(f"✓ Subdirectory in data path works: {path}")
        assert str(get_project_root() / "data" / "raw") in str(path)
        
        # Test subdirectory in output path
        path = get_output_path("subdir/plot.png", "figures")
        print(f"✓ Subdirectory in output path works: {path}")
        assert str(get_project_root() / "outputs" / "figures") in str(path)
        
        print("✓ Subdirectory usage tests PASSED\n")
        return True
    except Exception as e:
        print(f"✗ Subdirectory usage tests FAILED: {e}\n")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PATH TRAVERSAL VULNERABILITY FIX VALIDATION")
    print("Issue #04 - High - Path Traversal in Utils")
    print("=" * 60 + "\n")
    
    results = []
    results.append(("Normal Usage", test_normal_usage()))
    results.append(("Path Traversal Prevention", test_path_traversal_attempts()))
    results.append(("Output Path Prevention", test_output_path_traversal()))
    results.append(("Directory Type Validation", test_invalid_directory_types()))
    results.append(("Subdirectory Support", test_subdirectories()))
    
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED - Path traversal vulnerability is FIXED")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME TESTS FAILED - Review required")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
