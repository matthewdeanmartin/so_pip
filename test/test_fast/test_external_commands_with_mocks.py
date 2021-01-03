import os
from unittest.mock import patch

import so_pip.cli_clients.external_commands as commands


@patch("subprocess.run")
def test_pytest_detect(mock):
    print(commands.pytest_detect("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_pur(mock):
    print(commands.pur("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_safety(mock):
    print(commands.safety("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_pyflakes(mock):
    print(commands.pyflakes("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_black(mock):
    print(commands.black("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_pip_upgrade(mock):
    print(commands.pip_upgrade("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_pyupgrade(mock):
    print(commands.pyupgrade("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_futurize(mock):
    print(commands.futurize("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_pylint(mock):
    print(commands.pylint("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_pypinfo(mock):
    print(commands.pypinfo("foo.py"))
    assert mock.call_count == 0
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "abc"
    print(commands.pypinfo("foo.py"))
    assert mock.called and mock.call_count == 1
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


@patch("subprocess.run")
def test_two_to_three(mock):
    print(commands.two_to_three("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_execute_get_text(mock):
    print(commands.execute_get_text(["foo.py"]))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_generate_requirements(mock):
    print(commands.generate_requirements("foo.py"))
    assert mock.called and mock.call_count == 1


@patch("subprocess.run")
def test_isort(mock):
    print(commands.isort("foo.py"))
    assert mock.called and mock.call_count == 1
