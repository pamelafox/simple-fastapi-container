"""Test to ensure no unwanted dependencies are installed."""
import subprocess
import sys


def test_no_pandas_numpy_dependencies():
    """Verify that pandas and numpy are not installed as dependencies."""
    try:
        import pandas
        assert False, "pandas should not be installed as a dependency"
    except ImportError:
        pass  # This is expected

    try:
        import numpy
        assert False, "numpy should not be installed as a dependency"
    except ImportError:
        pass  # This is expected


def test_dependency_list():
    """Check that pandas and numpy are not in the installed packages."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list"],
        capture_output=True,
        text=True
    )
    
    packages = result.stdout.lower()
    assert "pandas" not in packages, "pandas found in installed packages"
    assert "numpy" not in packages, "numpy found in installed packages"


if __name__ == "__main__":
    test_no_pandas_numpy_dependencies()
    test_dependency_list()
    print("✓ No unwanted pandas/numpy dependencies found")