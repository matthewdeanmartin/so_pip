"""
So much python 2 on stackoverflow
"""
import os
import subprocess  # nosec

from so_pip.external_commands import pyupgrade, two_to_three
from so_pip.file_writing import find_file


def upgrade_string(code: str) -> str:
    """Upgrade a string to python three"""
    # if we don't upgrade the py2 crap, ast fails & all sorts of things fail.
    temp_file_name = find_file("tmp/upgrade.py", __file__)
    with open(temp_file_name, "w", encoding="utf-8", errors="replace") as temp:
        temp.write(code)
    try:
        two_to_three(temp_file_name)
    except subprocess.CalledProcessError as cpe:
        print("Can't covert to py3", str(cpe))
    # redundant... seems to do same things as 2to3
    # try:
    #     futurize(temp_file_name)
    # except subprocess.CalledProcessError as cpe:
    #     print("Can't covert to futurize")
    pyupgrade(temp_file_name)

    with open(temp_file_name, encoding="utf-8") as temp:
        code = temp.read()

    os.remove(temp_file_name)
    return code


def upgrade_file(submodule_name: str) -> None:
    """Upgrade a file to python 3"""
    try:
        two_to_three(submodule_name)
    except subprocess.CalledProcessError as cpe:
        print(f"2to3 failed: {submodule_name}", str(cpe))
    try:
        pyupgrade(submodule_name)
    except subprocess.CalledProcessError as cpe:
        print(f"pyupgrade failed : {submodule_name}", str(cpe))
