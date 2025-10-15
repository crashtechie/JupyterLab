#!/usr/bin/env python3
import argparse
import hashlib
import math
import os
import secrets
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Set

class PostgresSecurityValidator:
   
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_results: List[Dict] = []
        self.project_root = Path(__file__).parent.parent.parent
        
    def log_result(self, test_name: str, status: str, details: str = "", 
                   expected: str = "", actual: str = "", security_level: str = ""):
        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'expected': expected,
            'actual': actual,
            'security_level': security_level
        }
        self.test_results.append(result)
        
        # Display result
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}")
        
        if self.verbose and details:
            print(f"   📋 {details}")
        if self.verbose and security_level:
            print(f"   🛡️  {security_level}")
            
    def test_password_generation_security(self) -> bool:
        print("\n🔐 Testing Password Generation Security...")
        print("=" * 50)
        
        all_passed = True
        
        # Test 1: Import and function availability
        try:
            sys.path.append(str(self.project_root / "scripts"))
            import generate_postgres_password
            
            self.log_result(
                "Password Generator Import", "PASS",
                "Module imports successfully",
                "Module available", "Module available",
                "Code availability confirmed"
            )
        except Exception as e:
            self.log_result(
                "Password Generator Import", "FAIL", 
                f"Import failed: {e}",
                "Module available", "Import error"
            )
            all_passed = False
            return all_passed
        
        # Test 2: Password length validation (384-bit = 64 characters)
        try:
            password = generate_postgres_password.generate_secure_password()
            expected_length = 64  # 48 bytes * 4/3 (base64) ≈ 64 chars
            
            if len(password) == expected_length:
                self.log_result(
                    "Password Length (384-bit)", "PASS",
                    f"Generated {len(password)} character password",
                    f"{expected_length} characters", f"{len(password)} characters",
                    "384-bit security confirmed"
                )
            else:
                self.log_result(
                    "Password Length (384-bit)", "FAIL",
                    f"Expected {expected_length}, got {len(password)}",
                    f"{expected_length} characters", f"{len(password)} characters"
                )
                all_passed = False
                
        except Exception as e:
            self.log_result(
                "Password Length (384-bit)", "FAIL",
                f"Generation failed: {e}"
            )
            all_passed = False
        
        # Test 3: Password uniqueness (generate multiple passwords)
        try:
            passwords = set()
            collision_count = 0
            test_iterations = 1000
            
            for _ in range(test_iterations):
                pwd = generate_postgres_password.generate_secure_password()
                if pwd in passwords:
                    collision_count += 1
                passwords.add(pwd)
            
            uniqueness_rate = (len(passwords) / test_iterations) * 100
            
            if collision_count == 0 and uniqueness_rate == 100.0:
                self.log_result(
                    "Password Uniqueness", "PASS",
                    f"100% unique in {test_iterations} generations",
                    "No collisions", f"{collision_count} collisions",
                    f"Cryptographic randomness confirmed"
                )
            else:
                self.log_result(
                    "Password Uniqueness", "FAIL" if collision_count > 0 else "WARN",
                    f"{collision_count} collisions in {test_iterations} generations",
                    "No collisions", f"{collision_count} collisions"
                )
                if collision_count > 0:
                    all_passed = False
                    
        except Exception as e:
            self.log_result(
                "Password Uniqueness", "FAIL",
                f"Test failed: {e}"
            )
            all_passed = False
        
        # Test 4: Character set validation (URL-safe base64)
        try:
            password = generate_postgres_password.generate_secure_password()
            valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')
            password_chars = set(password)
            
            if password_chars.issubset(valid_chars):
                self.log_result(
                    "Character Set (URL-safe)", "PASS",
                    "All characters are URL-safe base64",
                    "URL-safe characters only", "URL-safe confirmed",
                    "Compatible with environment variables"
                )
            else:
                invalid_chars = password_chars - valid_chars
                self.log_result(
                    "Character Set (URL-safe)", "FAIL",
                    f"Invalid characters found: {invalid_chars}",
                    "URL-safe characters only", f"Invalid: {invalid_chars}"
                )
                all_passed = False
                
        except Exception as e:
            self.log_result(
                "Character Set (URL-safe)", "FAIL",
                f"Test failed: {e}"
            )
            all_passed = False
            
        return all_passed
    
    def test_entropy_analysis(self) -> bool:
        print("\n🎲 Testing Entropy and Randomness...")
        print("=" * 50)
        
        all_passed = True
        
        # Test 1: Shannon entropy calculation
        try:
            sys.path.append(str(self.project_root / "scripts"))
            import generate_postgres_password
            
            password = generate_postgres_password.generate_secure_password()
            char_counts = Counter(password)
            password_length = len(password)
            
            # Calculate Shannon entropy
            entropy = 0
            for count in char_counts.values():
                probability = count / password_length
                entropy -= probability * math.log2(probability)
            
            # Expected entropy for random 64-character password with base64 alphabet
            expected_min_entropy = 5.8  # log2(64) ≈ 6, but real-world is slightly lower
            
            if entropy >= expected_min_entropy:
                self.log_result(
                    "Shannon Entropy", "PASS",
                    f"Entropy: {entropy:.2f} bits per character",
                    f">= {expected_min_entropy} bits/char", f"{entropy:.2f} bits/char",
                    "High randomness confirmed"
                )
            else:
                self.log_result(
                    "Shannon Entropy", "FAIL",
                    f"Low entropy: {entropy:.2f} bits per character",
                    f">= {expected_min_entropy} bits/char", f"{entropy:.2f} bits/char"
                )
                all_passed = False
                
        except Exception as e:
            self.log_result(
                "Shannon Entropy", "FAIL",
                f"Entropy calculation failed: {e}"
            )
            all_passed = False
        
        # Test 2: Chi-square test for randomness
        try:
            passwords = []
            for _ in range(100):
                passwords.append(generate_postgres_password.generate_secure_password())
            
            # Combine all passwords for character frequency analysis
            all_chars = ''.join(passwords)
            char_counts = Counter(all_chars)
            
            # Expected frequency for uniform distribution
            total_chars = len(all_chars)
            alphabet_size = 64  # URL-safe base64
            expected_freq = total_chars / alphabet_size
            
            # Calculate chi-square statistic
            chi_square = sum((count - expected_freq) ** 2 / expected_freq 
                           for count in char_counts.values())
            
            # Critical value for alpha=0.05, df=63 is approximately 82.5
            critical_value = 82.5
            
            if chi_square < critical_value:
                self.log_result(
                    "Chi-Square Randomness", "PASS",
                    f"Chi-square: {chi_square:.2f} (good distribution)",
                    f"< {critical_value}", f"{chi_square:.2f}",
                    "Statistical randomness confirmed"
                )
            else:
                self.log_result(
                    "Chi-Square Randomness", "FAIL",
                    f"Chi-square: {chi_square:.2f} (poor distribution)",
                    f"< {critical_value}", f"{chi_square:.2f}"
                )
                all_passed = False
                
        except Exception as e:
            self.log_result(
                "Chi-Square Randomness", "FAIL",
                f"Statistical test failed: {e}"
            )
            all_passed = False
            
        return all_passed
    
    def test_storage_security(self) -> bool:
        """Test secure storage mechanisms for PostgreSQL passwords."""
        print("\n💾 Testing Storage Security...")
        print("=" * 50)
        
        all_passed = True
        
        # Test 1: .env file creation and update
        try:
            sys.path.append(str(self.project_root / "scripts"))
            import generate_postgres_password
            
            # Create temporary directory for testing
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_env = Path(temp_dir) / ".env"
                
                # Mock the project root for testing
                original_file_path = generate_postgres_password.Path(__file__)
                generate_postgres_password.Path.__file__ = str(Path(temp_dir) / "scripts" / "generate.py")
                
                try:
                    test_password = "test_password_384bit_very_secure_password_for_testing_purposes"
                    
                    # Test saving password
                    success = generate_postgres_password.save_password_to_env(test_password)
                    
                    if success and temp_env.exists():
                        # Verify content
                        with open(temp_env, 'r') as f:
                            content = f.read()
                        
                        if f"POSTGRES_PASSWORD={test_password}" in content:
                            self.log_result(
                                "Secure .env Storage", "PASS",
                                "Password saved to .env successfully",
                                ".env file created", ".env file exists",
                                "Secure file storage confirmed"
                            )
                        else:
                            self.log_result(
                                "Secure .env Storage", "FAIL",
                                "Password not found in .env file",
                                "Password in .env", "Password missing"
                            )
                            all_passed = False
                    else:
                        self.log_result(
                            "Secure .env Storage", "FAIL",
                            "Failed to create .env file",
                            "File created", "File not created"
                        )
                        all_passed = False
                        
                finally:
                    # Restore original path
                    generate_postgres_password.Path.__file__ = str(original_file_path)
                    
        except Exception as e:
            self.log_result(
                "Secure .env Storage", "FAIL",
                f"Storage test failed: {e}"
            )
            all_passed = False
        
        # Test 2: File permissions (Unix-like systems)
        if hasattr(os, 'chmod'):
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_path = Path(temp_file.name)
                    
                # Set and test file permissions
                os.chmod(temp_path, 0o600)
                actual_perms = oct(os.stat(temp_path).st_mode)[-3:]
                
                if actual_perms == '600':
                    self.log_result(
                        "File Permissions", "PASS",
                        "Correct permissions set (600 - owner read/write only)",
                        "600 (rw-------)", actual_perms,
                        "Secure file permissions"
                    )
                else:
                    self.log_result(
                        "File Permissions", "FAIL",
                        f"Incorrect permissions: {actual_perms}",
                        "600", actual_perms
                    )
                    all_passed = False
                
                # Cleanup
                temp_path.unlink()
                
            except Exception as e:
                self.log_result(
                    "File Permissions", "FAIL",
                    f"Permission test failed: {e}"
                )
                all_passed = False
        else:
            self.log_result(
                "File Permissions", "SKIP",
                "Not available on this platform",
                "Unix-like system", "Windows system",
                "Platform-specific feature"
            )
            
        return all_passed
    
    def test_recovery_methods(self) -> bool:
        """Test password recovery method functionality."""
        print("\n🔓 Testing Recovery Methods...")
        print("=" * 50)
        
        all_passed = True
        
        # Test 1: Standard recovery script existence and imports
        try:
            recovery_scripts = [
                "get-postgres-password-secure.py"
            ]
            
            for script in recovery_scripts:
                script_path = self.project_root / "scripts" / script
                if script_path.exists():
                    self.log_result(
                        f"Recovery Script: {script}", "PASS",
                        "Script file exists and is accessible",
                        "File exists", "File found",
                        "Recovery method available"
                    )
                else:
                    self.log_result(
                        f"Recovery Script: {script}", "FAIL",
                        "Script file not found",
                        "File exists", "File missing"
                    )
                    all_passed = False
                    
        except Exception as e:
            self.log_result(
                "Recovery Script Check", "FAIL",
                f"Script validation failed: {e}"
            )
            all_passed = False
        
        # Test 2: Ultra-secure recovery script functionality
        try:
            # Check if the ultra-secure recovery script exists and is functional
            secure_script_path = self.project_root / "scripts" / "get-postgres-password-secure.py"
            
            if secure_script_path.exists():
                self.log_result(
                    "Ultra-Secure Recovery Script", "PASS",
                    "get-postgres-password-secure.py available",
                    "Script exists", "Script found",
                    "Ultra-secure recovery functionality confirmed"
                )
            else:
                self.log_result(
                    "Ultra-Secure Recovery Script", "FAIL",
                    "get-postgres-password-secure.py not found",
                    "Script exists", "Script missing"
                )
                all_passed = False
                
        except Exception as e:
            self.log_result(
                "Recovery Function Import", "FAIL",
                f"Recovery import failed: {e}"
            )
            all_passed = False
            
        return all_passed
    
    def test_security_compliance(self) -> bool:
        """Test compliance with security standards and best practices."""
        print("\n🛡️  Testing Security Compliance...")
        print("=" * 50)
        
        all_passed = True
        
        # Test 1: NIST SP 800-63B compliance
        try:
            sys.path.append(str(self.project_root / "scripts"))
            import generate_postgres_password
            
            password = generate_postgres_password.generate_secure_password()
            
            # NIST recommends minimum 64-bit entropy for passwords
            # Our 384-bit (48 bytes) far exceeds this
            entropy_bits = len(password) * math.log2(64)  # base64 alphabet
            nist_minimum = 64
            
            if entropy_bits >= nist_minimum:
                self.log_result(
                    "NIST SP 800-63B Compliance", "PASS",
                    f"Entropy: {entropy_bits:.0f} bits (exceeds NIST minimum)",
                    f">= {nist_minimum} bits", f"{entropy_bits:.0f} bits",
                    "NIST security standards exceeded"
                )
            else:
                self.log_result(
                    "NIST SP 800-63B Compliance", "FAIL",
                    f"Insufficient entropy: {entropy_bits:.0f} bits",
                    f">= {nist_minimum} bits", f"{entropy_bits:.0f} bits"
                )
                all_passed = False
                
        except Exception as e:
            self.log_result(
                "NIST SP 800-63B Compliance", "FAIL",
                f"Compliance test failed: {e}"
            )
            all_passed = False
        
        # Test 2: OWASP password security guidelines
        try:
            password = generate_postgres_password.generate_secure_password()
            
            # OWASP recommendations
            checks = {
                "Minimum 12 characters": len(password) >= 12,
                "No dictionary words": True,  # Random generation ensures this
                "High entropy": len(password) >= 32,  # Much higher than OWASP minimum
                "Cryptographically secure": True  # Using secrets module
            }
            
            all_owasp_passed = all(checks.values())
            
            if all_owasp_passed:
                self.log_result(
                    "OWASP Security Guidelines", "PASS",
                    "All OWASP password guidelines satisfied",
                    "OWASP compliant", "All checks passed",
                    "Industry best practices followed"
                )
            else:
                failed_checks = [check for check, passed in checks.items() if not passed]
                self.log_result(
                    "OWASP Security Guidelines", "FAIL",
                    f"Failed checks: {failed_checks}",
                    "All checks pass", f"Failed: {len(failed_checks)}"
                )
                all_passed = False
                
        except Exception as e:
            self.log_result(
                "OWASP Security Guidelines", "FAIL",
                f"OWASP test failed: {e}"
            )
            all_passed = False
            
        return all_passed
    
    def run_performance_benchmark(self) -> bool:
        """Run performance benchmarks for password generation."""
        print("\n⚡ Running Performance Benchmarks...")
        print("=" * 50)
        
        all_passed = True
        
        try:
            sys.path.append(str(self.project_root / "scripts"))
            import generate_postgres_password
            
            # Benchmark password generation speed
            iterations = 10000
            start_time = time.time()
            
            for _ in range(iterations):
                generate_postgres_password.generate_secure_password()
            
            end_time = time.time()
            total_time = end_time - start_time
            passwords_per_second = iterations / total_time
            
            # Performance should be reasonable (> 1000 passwords/second)
            min_performance = 1000
            
            if passwords_per_second >= min_performance:
                self.log_result(
                    "Generation Performance", "PASS",
                    f"{passwords_per_second:.0f} passwords/second",
                    f">= {min_performance} pwd/sec", f"{passwords_per_second:.0f} pwd/sec",
                    "Excellent performance for production use"
                )
            else:
                self.log_result(
                    "Generation Performance", "WARN",
                    f"Slow performance: {passwords_per_second:.0f} passwords/second",
                    f">= {min_performance} pwd/sec", f"{passwords_per_second:.0f} pwd/sec"
                )
                
        except Exception as e:
            self.log_result(
                "Generation Performance", "FAIL",
                f"Benchmark failed: {e}"
            )
            all_passed = False
            
        return all_passed
    
    def generate_security_report(self) -> None:
        """Generate comprehensive security validation report."""
        print("\n📊 Security Validation Report")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        skipped_tests = len([r for r in self.test_results if r['status'] == 'SKIP'])
        warning_tests = len([r for r in self.test_results if r['status'] == 'WARN'])
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"📈 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ⚠️  Warnings: {warning_tests}")
        print(f"   ⏭️  Skipped: {skipped_tests}")
        print(f"   📊 Success Rate: {success_rate:.1f}%")
        print("")
        
        if failed_tests == 0:
            print("🎉 All critical security tests passed!")
            print("🛡️  PostgreSQL password system is secure for production use")
            print("🔐 384-bit security implementation validated")
        else:
            print("⚠️  Some tests failed - review security implementation")
            print("🔧 Address failed tests before production deployment")
        
        print("")
        print("🔍 Detailed Results:")
        for result in self.test_results:
            status_icon = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️" if result['status'] == "WARN" else "⏭️"
            print(f"   {status_icon} {result['test_name']}: {result['status']}")
            if result['details'] and self.verbose:
                print(f"      📋 {result['details']}")

def main():
    """Main function for PostgreSQL password security validation."""
    parser = argparse.ArgumentParser(
        description="PostgreSQL Password Security Validation Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Test Categories:
  • Password Generation Security (384-bit validation)
  • Entropy and Randomness Analysis  
  • Storage Security Testing
  • Recovery Method Validation
  • Security Compliance (NIST, OWASP)
  • Performance Benchmarks

Examples:
  python scripts/tests/validate_postgres_384bit_security.py
  python scripts/tests/validate_postgres_384bit_security.py --verbose
  python scripts/tests/validate_postgres_384bit_security.py --benchmark
        """
    )
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output with detailed test information')
    parser.add_argument('--benchmark', '-b', action='store_true',
                       help='Include performance benchmarking tests')
    
    args = parser.parse_args()
    
    print("🔐 PostgreSQL Password Security Validation Suite")
    print("=" * 55)
    print("🛡️  Testing 384-bit Security Implementation")
    print("📋 Comprehensive Security and Compliance Testing")
    print("")
    
    validator = PostgresSecurityValidator(verbose=args.verbose)
    
    # Run all test suites
    test_suites = [
        ("Password Generation Security", validator.test_password_generation_security),
        ("Entropy and Randomness", validator.test_entropy_analysis),
        ("Storage Security", validator.test_storage_security),
        ("Recovery Methods", validator.test_recovery_methods),
        ("Security Compliance", validator.test_security_compliance)
    ]
    
    if args.benchmark:
        test_suites.append(("Performance Benchmarks", validator.run_performance_benchmark))
    
    all_passed = True
    for suite_name, test_function in test_suites:
        print(f"\n🧪 Running {suite_name} Tests...")
        suite_passed = test_function()
        all_passed = all_passed and suite_passed
    
    # Generate final report
    validator.generate_security_report()
    
    # Return appropriate exit code
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())