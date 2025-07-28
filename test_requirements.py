#!/usr/bin/env python3
"""
Test script to validate uvicorn upgrade requirements.
Run this script to verify the dependency installation works.
"""

import subprocess
import sys
import tempfile
import os

def test_requirements_installation():
    """Test if the updated requirements can be installed successfully."""
    print("Testing uvicorn upgrade requirements installation...")
    
    # Create a temporary virtual environment
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = os.path.join(temp_dir, "test_venv")
        
        try:
            # Create virtual environment
            print("Creating test virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            
            # Get pip path
            if os.name == "nt":  # Windows
                pip_path = os.path.join(venv_path, "Scripts", "pip")
                python_path = os.path.join(venv_path, "Scripts", "python")
            else:  # Unix/Linux/Mac
                pip_path = os.path.join(venv_path, "bin", "pip")
                python_path = os.path.join(venv_path, "bin", "python")
            
            # Upgrade pip
            print("Upgrading pip...")
            subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            
            # Install requirements
            print("Installing requirements...")
            subprocess.run([pip_path, "install", "-r", "src/requirements.txt"], 
                         check=True, capture_output=True)
            
            # Test import
            print("Testing imports...")
            result = subprocess.run([
                python_path, "-c", 
                "import fastapi; import uvicorn; import gunicorn; print('✓ All imports successful')"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Requirements installation test PASSED")
                print(result.stdout)
                return True
            else:
                print("✗ Import test failed:")
                print(result.stderr)
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"✗ Installation failed: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False

if __name__ == "__main__":
    print("=" * 50)
    print("Uvicorn Upgrade Requirements Test")
    print("=" * 50)
    
    success = test_requirements_installation()
    
    if success:
        print("\n✓ SUCCESS: Requirements can be installed without conflicts!")
        sys.exit(0)
    else:
        print("\n✗ FAILURE: Requirements installation failed!")
        sys.exit(1)