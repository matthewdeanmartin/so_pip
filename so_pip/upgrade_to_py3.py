"""
So much python 2 on stackoverflow
"""
import os
import subprocess

from so_pip.external_commands import pyupgrade, two_to_three


def upgrade_string(code: str) -> str:
    """Upgrade a string to python three"""
    # if we don't upgrade the py2 crap, ast fails & all sorts of things fail.
    with open("tmp/upgrade.py", "w", encoding="utf-8", errors="replace") as temp:
        temp.write(code)
    try:
        two_to_three("tmp/upgrade.py", "pipenv run")
    except subprocess.CalledProcessError as cpe:
        print("Can't covert to py3", str(cpe))
    # redundant... seems to do same things as 2to3
    # try:
    #     futurize("tmp/upgrade.py", "pipenv run")
    # except subprocess.CalledProcessError as cpe:
    #     print("Can't covert to futurize")
    pyupgrade("tmp/upgrade.py", "pipenv run")

    with open("tmp/upgrade.py", encoding="utf-8") as temp:
        code = temp.read()

    os.remove("tmp/upgrade.py")
    return code


def upgrade_file(submodule_name: str) -> None:
    """Upgrade a file to python 3"""
    try:
        two_to_three(submodule_name, "pipenv run")
    except subprocess.CalledProcessError as cpe:
        print(f"2to3 failed: {submodule_name}", str(cpe))
    try:
        pyupgrade(submodule_name, "pipenv run")
    except subprocess.CalledProcessError as cpe:
        print(f"pyupgrade failed : {submodule_name}", str(cpe))
