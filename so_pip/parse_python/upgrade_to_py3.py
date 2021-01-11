"""
So much python 2 on stackoverflow
"""
import logging
import subprocess  # nosec
import tempfile

from so_pip.cli_clients.external_commands import pyupgrade, two_to_three

LOGGER = logging.getLogger(__name__)


def upgrade_string(code: str) -> str:
    """Upgrade a string to python three"""
    # if we don't upgrade the py2 crap, ast fails & all sorts of things fail.
    at_least_one_worked = False
    with tempfile.TemporaryDirectory(prefix="upgrade_py") as temp_dir:
        temp_file_name = temp_dir.replace("\\", "/") + "/upgrade.py"
        with open(temp_file_name, mode="w", encoding="utf-8", errors="replace") as temp:
            temp.write(code)
        try:
            two_to_three(temp_file_name)
            at_least_one_worked = True
        except subprocess.CalledProcessError as cpe:
            LOGGER.debug("Can't covert to py3: " + str(cpe))
        # redundant... seems to do same things as 2to3
        # try:
        #     futurize(temp_file_name)
        # except subprocess.CalledProcessError as cpe:
        #     print("Can't covert to futurize")
        try:
            pyupgrade(temp_file_name)
            at_least_one_worked = True
        except subprocess.CalledProcessError as cpe:
            LOGGER.debug("Can't pyupgrade " + str(cpe))

        if at_least_one_worked:
            with open(temp_file_name, encoding="utf-8") as temp:
                code = temp.read()

    return code


def upgrade_file(submodule_name: str) -> None:
    """Upgrade a file to python 3"""
    try:
        two_to_three(submodule_name)
    except subprocess.CalledProcessError as cpe:
        LOGGER.debug(f"2to3 failed: {submodule_name} " + str(cpe))
    try:
        pyupgrade(submodule_name)
    except subprocess.CalledProcessError as cpe:
        LOGGER.debug(f"pyupgrade failed : {submodule_name} " + str(cpe))
