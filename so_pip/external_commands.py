"""
Shell out to run a few commands
"""
import os
import shlex
import subprocess  # nosec
from typing import Dict, List, Optional

RUNNING_IN_VENV = "VIRTUAL_ENV" in os.environ


def generate_requirements(folder: str, shell: str) -> str:
    """Make more installable"""
    if RUNNING_IN_VENV:
        shell = ""
    command = shlex.split(
        f"{shell} pipreqs {folder} --force".strip().replace("  ", " ")
    )
    print(command)
    result = execute_get_text(command)
    return result


def futurize(file_name: str, shell: str) -> str:
    """Yet another py2 to 3 converter"""
    if RUNNING_IN_VENV:
        shell = ""
    text = f"{shell} futurize --stage1 -w {file_name}"
    print(text)
    command = shlex.split(text)
    result = execute_get_text(command)
    print(result)
    return result


def two_to_three(file_name: str, shell: str) -> str:
    """fix print"""
    if RUNNING_IN_VENV:
        shell = ""
    text = f"{shell} 2to3 -w {file_name}"
    print(text)
    command = shlex.split(text)
    result = execute_get_text(command)
    print(result)
    return result


def pyupgrade(file_name: str, shell: str) -> str:
    """Bump to 3.7+"""
    if RUNNING_IN_VENV:
        shell = ""
    command = (
        f"{shell} pyupgrade "
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
    # shell: bool = True, # causes cross plat probs, security warnings, etc.
    env: Optional[Dict[str, str]] = None,
) -> str:
    """
    Execute shell command and return stdout txt
    """
    if env is None:
        env = {}

    completed = None
    try:
        completed = subprocess.run(  # nosec
            command,
            check=not ignore_error,
            # shell=shell, # causes cross plat probs, security warnings, etc.
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # env=env,
        )
    except subprocess.CalledProcessError:
        if ignore_error and completed:
            return completed.stdout.decode("utf-8") + completed.stderr.decode("utf-8")
        raise
    else:
        return completed.stdout.decode("utf-8") + completed.stderr.decode("utf-8")


def isort(folder: str, shell: str) -> str:
    """Sort the imports to discover import order bugs and prevent import order bugs"""
    # This must run before black. black doesn't change import order but it wins
    # any arguments about formatting.
    # isort MUST be installed with pipx! It is not compatible with pylint in the same
    # venv. Maybe someday, but it just isn't worth the effort.

    command = f"{shell} isort --profile black {folder}"
    print(command)
    parts = shlex.split(command)
    result = execute_get_text(parts)
    print(result)
    return result
