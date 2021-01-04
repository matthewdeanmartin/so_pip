"""
Using source code, find requirements.

Removes python 3.8 system libraries.

Assumes module names match package names. This is not true.

Does not run safety if no modules are successfully guessed.
"""
import logging
import os
import subprocess  # nosec
from typing import Optional, Tuple

from stdlib_list import stdlib_list

from so_pip import settings as settings

# noinspection PyProtectedMember
from so_pip._vendor.find_imports.main import find_imports

# ^\s*(from|import)\s+\w+
from so_pip.cli_clients.external_commands import generate_requirements
from so_pip.models.python_package_model import PythonPackage
from so_pip.pypi_query.main import find_modules
from so_pip.support_files.setup_cfg import create_setup_cfg

# https://github.com/ohjeah/pip-validate

LOGGER = logging.getLogger(__name__)


def requirements_for_file(
    package_folder: str, python_submodule: PythonPackage
) -> Tuple[Optional[str], int]:
    """Requirements for running `safety`"""

    package_count = 0
    file_to_write = None
    all_imports = []
    with os.scandir(package_folder) as root_dir:
        for path in root_dir:
            if path.is_file():
                filename = path.name
                # for filename in os.listdir(package_folder):
                if "." not in filename:
                    raise TypeError("All files must have an extension")
                if filename.endswith(".py"):
                    py_file = path.path
                    all_imports += find_imports(py_file)
                else:
                    continue

    # remove built ins
    libraries = stdlib_list("3.8")
    python_submodule.dependencies = set(all_imports) - set(libraries)

    packages_of_same_name, not_in_pypi = find_modules(
        list(python_submodule.dependencies)
    )

    # https://stackoverflow.com/questions/8370206/how-to-get-a-list-of-built-in-modules-in-python
    if python_submodule.dependencies:
        file_to_write = package_folder + "/requirements.txt"
        with open(
            file_to_write, "w", encoding="utf-8", errors="replace"
        ) as requirements:
            requirements.write("# module names often don't match package names!\n\n")
            for _import in packages_of_same_name:
                requirements.write(_import + "\n")
                package_count += 1
            for bad_import in not_in_pypi:
                item = f"# {bad_import} # module imported but no package of same name\n"
                requirements.write(item)

    if settings.GENERATE_SETUP_CFG:
        create_setup_cfg(package_folder, python_submodule)
    return file_to_write, package_count


def process_requirements_for_a_module(package_folder: str) -> None:
    """
    Call a commandline requirements generator
    """
    if settings.GENERATE_REQUIREMENTS_TXT:
        try:
            generate_requirements(package_folder)
        except subprocess.CalledProcessError as cpe:
            LOGGER.debug(f"generate requirements failed : {package_folder}", str(cpe))
