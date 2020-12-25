"""
Shell out to run a few commands
"""
import shlex
import subprocess  # nosec
from typing import Dict, List, Optional

from so_pip.file_writing import find_file
from so_pip.settings import SHELL


def pyflakes(file: str) -> str:
    """Just run pyflakes"""
    command = shlex.split(f"{SHELL} pyflakes {file}".strip().replace("  ", " "))
    print(command)
    result = execute_get_text(command)
    return result


def generate_requirements(folder: str) -> str:
    """Make more installable"""
    command = shlex.split(
        f"{SHELL} pipreqs {folder} --force".strip().replace("  ", " ")
    )
    print(command)
    result = execute_get_text(command)
    return result


def futurize(file_name: str) -> str:
    """Yet another py2 to 3 converter"""
    text = f"{SHELL} futurize --stage1 -w {file_name}"
    print(text)
    command = shlex.split(text)
    result = execute_get_text(command)
    print(result)
    return result


def two_to_three(file_name: str) -> str:
    """fix print"""
    text = f"{SHELL} 2to3 -w {file_name}"
    print(text)
    command = shlex.split(text)
    result = execute_get_text(command)
    print(result)
    return result


def pyupgrade(file_name: str) -> str:
    """Bump to 3.7+"""
    command = (
        f"{SHELL} pyupgrade "
        f"--py37-plus "
        f"--exit-zero-even-if-changed {file_name}".strip().replace("  ", " ")
    )
    print(command)
    parts = shlex.split(command)

    result = execute_get_text(parts, ignore_error=False)
    print(result)
    return result


def execute_get_text(
    command: List[str],
    ignore_error: bool = False,
    # shell: bool = True, # causes cross plat problems, security warnings, etc.
    env: Optional[Dict[str, str]] = None,
) -> str:
    """
    Execute shell command and return stdout txt
    """

    completed = None
    try:
        completed = subprocess.run(  # nosec
            command,
            check=not ignore_error,
            # shell=shell, # causes cross plat problems, security warnings, etc.
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
    except subprocess.CalledProcessError:
        if ignore_error and completed:
            return completed.stdout.decode("utf-8") + completed.stderr.decode("utf-8")
        raise
    else:
        return completed.stdout.decode("utf-8") + completed.stderr.decode("utf-8")


def isort(folder: str) -> str:
    """Sort the imports to discover import order bugs and prevent import order bugs"""
    # This must run before black. black doesn't change import order but it wins
    # any arguments about formatting.
    # isort MUST be installed with pipx! It is not compatible with pylint in the same
    # venv. Maybe someday, but it just isn't worth the effort.

    command = f"{SHELL} isort --profile black {folder}"
    print(command)
    parts = shlex.split(command)
    result = execute_get_text(parts)
    print(result)
    return result


def pylint(folder: str) -> str:
    """Sort the imports to discover import order bugs and prevent import order bugs"""
    # This must run before black. black doesn't change import order but it wins
    # any arguments about formatting.
    # isort MUST be installed with pipx! It is not compatible with pylint in the same
    # venv. Maybe someday, but it just isn't worth the effort.
    rcfile = find_file("pylintrc.ini", __file__)
    command = (
        f"{SHELL} pylint "
        "--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' "
        f"--exit-zero --rcfile='{rcfile}' {folder}".strip().replace("  ", " ")
    )
    "".strip().replace("  ", " ")
    print(command)
    parts = shlex.split(command)
    result = execute_get_text(parts)
    print(result)
    return result
