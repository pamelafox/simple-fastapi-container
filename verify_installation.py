#!/usr/bin/env python3
"""
Verification script for the gunicorn upgrade fix.
This script verifies that the upgraded dependencies can be installed and work correctly.
"""

import sys
import subprocess
import os

def run_command(cmd, description):
    """Run a command and return True if successful."""
    print(f"\n🔍 {description}")
    print(f"Running: {cmd}")
    try:
        # Use bash explicitly for source command
        if 'source' in cmd:
            cmd = f"bash -c '{cmd}'"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main verification function."""
    print("🚀 Starting installation verification for gunicorn upgrade fix...")
    
    # Change to the repository directory
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)
    print(f"Working directory: {repo_dir}")
    
    success = True
    
    # Create a virtual environment
    if not run_command("python3 -m venv .venv_verify", "Creating verification virtual environment"):
        return False
    
    # Install requirements-dev.txt (which includes src/requirements.txt)
    if not run_command("source .venv_verify/bin/activate && pip install --upgrade pip", "Upgrading pip"):
        success = False
    
    if not run_command("source .venv_verify/bin/activate && pip install -r requirements-dev.txt", "Installing dev requirements"):
        success = False
    
    # Check that gunicorn installed correctly
    if not run_command("source .venv_verify/bin/activate && python -c 'import gunicorn; print(f\"Gunicorn version: {gunicorn.__version__}\")'", "Checking gunicorn installation"):
        success = False
    
    # Run the tests
    if not run_command("source .venv_verify/bin/activate && python -m pytest src/gunicorn_test.py -v", "Running gunicorn test"):
        success = False
    
    # Run all tests
    if not run_command("source .venv_verify/bin/activate && python -m pytest -v", "Running all tests"):
        success = False
    
    # Test the FastAPI application can start
    if not run_command("source .venv_verify/bin/activate && python -c 'from src.api.main import app; print(\"✅ FastAPI app imports correctly\")'", "Testing FastAPI app import"):
        success = False
    
    # Test gunicorn configuration check
    if not run_command("source .venv_verify/bin/activate && cd src && gunicorn --check-config api.main:app", "Testing gunicorn config check"):
        success = False
    
    # Cleanup
    run_command("rm -rf .venv_verify", "Cleaning up verification environment")
    
    if success:
        print("\n🎉 All verification tests passed!")
        print("The gunicorn upgrade fix is working correctly.")
        print("\nTo install and verify manually:")
        print("1. python3 -m venv .venv")
        print("2. source .venv/bin/activate")  
        print("3. pip install -r requirements-dev.txt")
        print("4. python -m pytest")
        return True
    else:
        print("\n❌ Some verification tests failed.")
        print("Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)