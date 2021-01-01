"""
Shell out to run a few commands
"""
import logging
import os
import shlex

from so_pip import settings as settings
from so_pip.cli_clients.subprocess_utils import execute_get_text
from so_pip.utils.files_utils import find_file

LOGGER = logging.getLogger(__name__)


def pytest_detect(file: str) -> str:
    """How many tests in this file"""
    # so few SO questions have executable unit tests

    command_text = f"pytest {file} --collect-only".strip().replace("  ", " ")
    LOGGER.debug(command_text)
    command = shlex.split(command_text)
    result = execute_get_text(command)
    return result


# https://stackoverflow.com/questions/24764549/
# upgrade-python-packages-from-requirements-txt-using-pip-command
def pip_upgrade(file: str) -> str:
    """
    Get latest versions & pip
    """
    # pip-upgrade
    command_text = f"pip-upgrade --default-index-url --file {file}".strip().replace(
        "  ", " "
    )
    LOGGER.debug(command_text)
    command = shlex.split(command_text)
    result = execute_get_text(command)
    return result


def pur(file: str) -> str:
    """
    Get latest versions & pip
    """
    # alternative... this one upgrades pinned, too
    # https://github.com/alanhamlett/pip-update-requirements

    command_text = f"pur -f --requirement {file}".strip().replace("  ", " ")
    LOGGER.debug(command_text)
    command = shlex.split(command_text)
    result = execute_get_text(command)
    return result


def safety(file: str) -> str:
    """Check if dep is malicious/insecure"""
    command = shlex.split(f"safety check --file {file}".strip().replace("  ", " "))
    LOGGER.debug(command)
    result = execute_get_text(command)
    return result


def pyflakes(file: str) -> str:
    """Just run pyflakes"""
    command = shlex.split(
        f"{settings.SHELL} pyflakes {file}".strip().replace("  ", " ")
    )
    LOGGER.debug(command)
    result = execute_get_text(command)
    return result


def generate_requirements(folder: str) -> str:
    """Make more installable"""
    command = shlex.split(
        f"{settings.SHELL} pipreqs {folder} --force".strip().replace("  ", " ")
    )
    LOGGER.debug(command)
    result = execute_get_text(command)
    return result


def futurize(file_name: str) -> str:
    """Yet another py2 to 3 converter"""
    text = f"{settings.SHELL} futurize --stage1 -w {file_name}"
    LOGGER.debug(text)
    command = shlex.split(text)
    result = execute_get_text(command)
    LOGGER.debug(result)
    return result


def black(folder_name: str) -> str:
    """Format files to keep pylint happy"""
    text = f"{settings.SHELL} black {folder_name} --target-version=py38"
    LOGGER.debug(text)
    command = shlex.split(text)
    result = execute_get_text(command)
    LOGGER.debug(result)
    return result


def two_to_three(file_name: str) -> str:
    """fix print"""
    text = f"{settings.SHELL} 2to3 -w {file_name}"
    LOGGER.debug(text)
    command = shlex.split(text)
    result = execute_get_text(command)
    LOGGER.debug(result)
    return result


def pyupgrade(file_name: str) -> str:
    """Bump to 3.7+"""
    command = (
        f"{settings.SHELL} pyupgrade "
        f"--py37-plus "
        f"--exit-zero-even-if-changed {file_name}".strip().replace("  ", " ")
    )
    LOGGER.debug(command)
    parts = shlex.split(command)

    result = execute_get_text(parts, ignore_error=False)
    LOGGER.debug(result)
    return result


def isort(folder: str) -> str:
    """Sort the imports to discover import order bugs and prevent import order bugs"""
    # This must run before black. black doesn't change import order but it wins
    # any arguments about formatting.
    # isort MUST be installed with pipx! It is not compatible with pylint in the same
    # venv. Maybe someday, but it just isn't worth the effort.

    command = f"{settings.SHELL} isort --profile black {folder}"
    LOGGER.debug(command)
    parts = shlex.split(command)
    result = execute_get_text(parts)
    LOGGER.debug(result)
    return result


def pylint(folder: str) -> str:
    """Sort the imports to discover import order bugs and prevent import order bugs"""
    # This must run before black. black doesn't change import order but it wins
    # any arguments about formatting.
    # isort MUST be installed with pipx! It is not compatible with pylint in the same
    # venv. Maybe someday, but it just isn't worth the effort.
    rcfile = find_file("pylintrc.ini", __file__)

    command = (
        f"{settings.SHELL} pylint "
        "--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' "
        f"--exit-zero --rcfile='{rcfile}' {folder}".strip().replace("  ", " ")
    )
    "".strip().replace("  ", " ")
    LOGGER.debug(command)
    parts = shlex.split(command)
    result = execute_get_text(parts)
    LOGGER.debug(result)
    return result


def pypinfo(package: str) -> str:
    """
    Pypi info
    """
    # https://pypi.org/project/pypinfo/
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None):
        return (
            "You must set up credentials "
            "to run pypinfo https://pypi.org/project/pypinfo/"
        )
    command = f"{settings.SHELL} pypinfo {package}"
    LOGGER.debug(command)
    parts = shlex.split(command)
    result = execute_get_text(parts, ignore_error=True)
    LOGGER.debug(result)
    return result
