#!/usr/bin/env python3
"""
Docker Compose Jupyter Lab Setup Test Script

This script tests the Docker Compose configuration end-to-end to ensure
the Jupyter Lab environment is working correctly.
"""

import subprocess
import time
import requests
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class DockerJupyterTester:
    def __init__(self):
        self.base_url = "http://localhost:8888"
        self.token = "datascience-token"
        self.test_results = []
        self.project_root = Path(__file__).parent.parent.parent
        
    def log_test(self, test_name, status, message="", details=None):
        """Log test results"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "status": status,
            "message": message,
            "details": details or {}
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        
    def run_command(self, command, timeout=30):
        """Run a shell command and return result"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                cwd=self.project_root
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def test_docker_availability(self):
        """Test if Docker and Docker Compose are available"""
        success, stdout, stderr = self.run_command("docker --version")
        if success:
            docker_version = stdout.strip()
            self.log_test("Docker Availability", "PASS", docker_version)
        else:
            self.log_test("Docker Availability", "FAIL", f"Docker not available: {stderr}")
            return False
            
        success, stdout, stderr = self.run_command("docker compose version")
        if success:
            compose_version = stdout.strip()
            self.log_test("Docker Compose Availability", "PASS", compose_version)
            return True
        else:
            self.log_test("Docker Compose Availability", "FAIL", f"Docker Compose not available: {stderr}")
            return False
    
    def test_compose_file_syntax(self):
        """Test Docker Compose file syntax"""
        success, stdout, stderr = self.run_command("docker compose config")
        if success:
            self.log_test("Compose File Syntax", "PASS", "Configuration is valid")
            return True
        else:
            self.log_test("Compose File Syntax", "FAIL", f"Invalid configuration: {stderr}")
            return False
    
    def test_environment_file(self):
        """Test if .env file exists and has required variables"""
        env_file = self.project_root / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_content = f.read()
            
            required_vars = ["JUPYTER_TOKEN", "TZ"]
            missing_vars = []
            
            for var in required_vars:
                if var not in env_content:
                    missing_vars.append(var)
            
            if not missing_vars:
                self.log_test("Environment File", "PASS", "All required variables present")
                return True
            else:
                self.log_test("Environment File", "WARN", f"Missing variables: {missing_vars}")
                return True  # Not critical
        else:
            self.log_test("Environment File", "FAIL", ".env file not found")
            return False
    
    def start_services(self):
        """Start Docker Compose services"""
        print("\n🚀 Starting Docker Compose services...")
        success, stdout, stderr = self.run_command("docker compose up -d", timeout=120)
        
        if success:
            self.log_test("Service Startup", "PASS", "Services started successfully")
            # Wait for services to be ready
            time.sleep(10)
            return True
        else:
            self.log_test("Service Startup", "FAIL", f"Failed to start services: {stderr}")
            return False
    
    def test_container_running(self):
        """Test if Jupyter container is running"""
        success, stdout, stderr = self.run_command("docker compose ps")
        
        if success and "jupyterlab-datascience" in stdout:
            if "Up" in stdout:
                self.log_test("Container Status", "PASS", "Jupyter container is running")
                return True
            else:
                self.log_test("Container Status", "FAIL", "Jupyter container is not running")
                return False
        else:
            self.log_test("Container Status", "FAIL", f"Container check failed: {stderr}")
            return False
    
    def test_jupyter_accessibility(self):
        """Test if Jupyter Lab is accessible via HTTP"""
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/lab?token={self.token}", timeout=5)
                if response.status_code == 200:
                    self.log_test("Jupyter Accessibility", "PASS", f"Jupyter Lab accessible at {self.base_url}")
                    return True
            except requests.exceptions.RequestException:
                if attempt < max_attempts - 1:
                    time.sleep(5)
                    continue
        
        self.log_test("Jupyter Accessibility", "FAIL", f"Cannot access Jupyter Lab at {self.base_url}")
        return False
    
    def test_jupyter_api(self):
        """Test Jupyter API functionality"""
        try:
            # Test API endpoint
            response = requests.get(f"{self.base_url}/api/status?token={self.token}", timeout=10)
            if response.status_code == 200:
                status_data = response.json()
                self.log_test("Jupyter API", "PASS", "API responding correctly", status_data)
                return True
            else:
                self.log_test("Jupyter API", "FAIL", f"API returned status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Jupyter API", "FAIL", f"API test failed: {str(e)}")
            return False
    
    def test_volume_mounts(self):
        """Test if volume mounts are working correctly"""
        try:
            # Create a test file in notebooks directory
            test_file = self.project_root / "notebooks" / "test_volume_mount.txt"
            test_content = f"Volume mount test - {datetime.now().isoformat()}"
            
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            # Check if file appears in container
            success, stdout, stderr = self.run_command(
                "docker compose exec -T jupyter ls /home/jovyan/work/notebooks/"
            )
            
            if success and "test_volume_mount.txt" in stdout:
                # Clean up test file
                test_file.unlink()
                self.log_test("Volume Mounts", "PASS", "Volume mounts working correctly")
                return True
            else:
                self.log_test("Volume Mounts", "FAIL", f"Volume mount test failed: {stderr}")
                return False
                
        except Exception as e:
            self.log_test("Volume Mounts", "FAIL", f"Volume mount test error: {str(e)}")
            return False
    
    def test_python_environment(self):
        """Test Python environment and packages in container"""
        # Test basic Python execution
        success, stdout, stderr = self.run_command(
            'docker compose exec -T jupyter python -c "import sys; print(sys.version)"'
        )
        
        if success:
            python_version = stdout.strip()
            self.log_test("Python Environment", "PASS", f"Python version: {python_version}")
        else:
            self.log_test("Python Environment", "FAIL", f"Python test failed: {stderr}")
            return False
        
        # Test key data science packages
        packages_to_test = ["pandas", "numpy", "matplotlib", "seaborn", "plotly", "sklearn"]
        failed_packages = []
        
        for package in packages_to_test:
            success, stdout, stderr = self.run_command(
                f'docker compose exec -T jupyter python -c "import {package}; print({package}.__version__)"'
            )
            
            if not success:
                failed_packages.append(package)
        
        if not failed_packages:
            self.log_test("Data Science Packages", "PASS", "All key packages available")
            return True
        else:
            self.log_test("Data Science Packages", "FAIL", f"Missing packages: {failed_packages}")
            return False
    
    def create_test_notebook(self):
        """Create and execute a test notebook"""
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# Test notebook for Docker Compose setup\n",
                        "import pandas as pd\n",
                        "import numpy as np\n",
                        "import matplotlib.pyplot as plt\n",
                        "\n",
                        "# Create test data\n",
                        "data = {'x': range(10), 'y': np.random.randn(10)}\n",
                        "df = pd.DataFrame(data)\n",
                        "\n",
                        "print('Test notebook executed successfully!')\n",
                        "print(f'DataFrame shape: {df.shape}')\n",
                        "df.head()"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.8.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        # Save test notebook
        test_notebook_path = self.project_root / "notebooks" / "docker_test.ipynb"
        with open(test_notebook_path, 'w') as f:
            json.dump(notebook_content, f, indent=2)
        
        self.log_test("Test Notebook Creation", "PASS", "Test notebook created successfully")
        return True
    
    def stop_services(self):
        """Stop Docker Compose services"""
        print("\n🛑 Stopping Docker Compose services...")
        success, stdout, stderr = self.run_command("docker compose down")
        
        if success:
            self.log_test("Service Shutdown", "PASS", "Services stopped successfully")
            return True
        else:
            self.log_test("Service Shutdown", "FAIL", f"Failed to stop services: {stderr}")
            return False
    
    def save_results(self):
        """Save test results to file"""
        results_file = self.project_root / "scripts" / "tests" / "results" / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.test_results),
            "passed": len([r for r in self.test_results if r["status"] == "PASS"]),
            "failed": len([r for r in self.test_results if r["status"] == "FAIL"]),
            "warnings": len([r for r in self.test_results if r["status"] == "WARN"]),
            "test_results": self.test_results
        }
        
        with open(results_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Test results saved to: {results_file}")
        return summary
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🧪 Starting Docker Compose Jupyter Lab End-to-End Tests\n")
        
        # Pre-flight tests
        if not self.test_docker_availability():
            return False
        
        if not self.test_compose_file_syntax():
            return False
            
        self.test_environment_file()
        
        # Service tests
        if not self.start_services():
            return False
        
        try:
            # Wait for services to stabilize
            time.sleep(15)
            
            if not self.test_container_running():
                return False
            
            if not self.test_jupyter_accessibility():
                return False
            
            if not self.test_jupyter_api():
                return False
            
            if not self.test_volume_mounts():
                return False
            
            if not self.test_python_environment():
                return False
            
            self.create_test_notebook()
            
        finally:
            # Always try to stop services
            self.stop_services()
        
        # Generate summary
        summary = self.save_results()
        
        print(f"\n🏁 Test Summary:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Warnings: {summary['warnings']} ⚠️")
        
        success_rate = (summary['passed'] / summary['total_tests']) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return summary['failed'] == 0

if __name__ == "__main__":
    tester = DockerJupyterTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)