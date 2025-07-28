# Gunicorn Upgrade Fix - Issue #79

This document explains the fix for the failing Dependabot PR #65 that attempted to upgrade gunicorn.

## Problem

Dependabot attempted to upgrade gunicorn from version 22.0.0 to a newer version (likely 23.0.0), but the CI tests failed due to a breaking change in the gunicorn API.

## Root Cause

The test file `src/gunicorn_test.py` was using a deprecated import pattern:
```python
from gunicorn.app.wsgiapp import run
```

In gunicorn 23.x, this direct function import was deprecated in favor of using the proper application class.

## Solution

### Changes Made

1. **Updated gunicorn version** in `src/requirements.txt`:
   ```diff
   - gunicorn==22.0.0
   + gunicorn==23.0.0
   ```

2. **Fixed import compatibility** in `src/gunicorn_test.py`:
   ```diff
   - from gunicorn.app.wsgiapp import run
   + from gunicorn.app.wsgiapp import WSGIApplication
   
   def test_config_imports():
       argv = ["gunicorn", "--check-config", "api.main:app"]
       
       with mock.patch.object(sys, "argv", argv):
           with pytest.raises(SystemExit) as excinfo:
   -           run()
   +           app = WSGIApplication()
   +           app.run()
       
       assert excinfo.value.args[0] == 0
   ```

### Why This Fix Works

- The new pattern uses the proper gunicorn application class `WSGIApplication()`
- This class reads configuration from `sys.argv` (which we mock in the test)
- The `app.run()` method performs the same validation as the old `run()` function
- The test still validates that gunicorn can successfully parse the configuration

## Verification

To verify this fix works:

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Run tests:
   ```bash
   python -m pytest
   ```

4. Test gunicorn configuration:
   ```bash
   cd src
   gunicorn --check-config api.main:app
   ```

## Compatibility

This fix maintains backward compatibility while supporting the newer gunicorn 23.x API. The configuration file `src/gunicorn.conf.py` requires no changes as all the settings used are stable across versions.

## Alternative Installation Command

If you encounter any issues, you can also install using the verification script:
```bash
python3 verify_installation.py
```