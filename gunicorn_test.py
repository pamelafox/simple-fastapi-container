import sys
from unittest import mock

import pytest
from gunicorn.app.wsgiapp import run

def test_config_imports():
    argv = [
        "gunicorn",
        "--check-config",
        "api.main:app",
    ]
    mock_argv = mock.patch.object(sys, "argv", argv)

    with pytest.raises(SystemExit) as excinfo, mock_argv:
        run()

    assert excinfo.value.args[0] == 0