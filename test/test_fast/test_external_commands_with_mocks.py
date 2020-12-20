
from unittest.mock import patch

import so_pip.external_commands as commands


@patch('subprocess.run')
def test_pyupgrade(mock):
    print(commands.pyupgrade("foo.py", "pipenv run"))
    assert mock.called and mock.call_count ==1

@patch('subprocess.run')
def test_futurize(mock):
    print(commands.futurize("foo.py", "pipenv run"))
    assert mock.called and mock.call_count ==1

@patch('subprocess.run')
def test_two_to_three(mock):
    print(commands.two_to_three("foo.py", "pipenv run"))
    assert mock.called and mock.call_count ==1

@patch('subprocess.run')
def test_execute_get_text(mock):
    print(commands.execute_get_text(["foo.py"]))
    assert mock.called and mock.call_count ==1

@patch('subprocess.run')
def test_generate_requirements(mock):
    print(commands.generate_requirements("foo.py", "pipenv run"))
    assert mock.called and mock.call_count ==1

@patch('subprocess.run')
def test_isort(mock):
    print(commands.isort("foo.py", "pipenv run"))
    assert mock.called and mock.call_count ==1
