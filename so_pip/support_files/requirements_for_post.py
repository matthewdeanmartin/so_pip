"""
Using source code, find requirements.

Removes python 3.8 system libraries.

Assumes module names match package names. This is not true.

Does not run safety if no modules are successfully guessed.
"""
import os
import subprocess  # nosec
from typing import Tuple

from stdlib_list import stdlib_list

from so_pip import settings as settings


# ^\s*(from|import)\s+\w+
from so_pip.cli_clients.external_commands import generate_requirements
from so_pip.models.python_package_model import PythonPackage
from so_pip.pypi_query.main import find_modules
from so_pip.support_files.setup_py import render_setup_py
from so_pip_packages.find_imports import main as find_imports

# https://github.com/ohjeah/pip-validate


def requirements_for_file(package_folder: str, python_submodule: PythonPackage) -> Tuple[str, int]:
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
                    all_imports += find_imports.find_imports(py_file)
                else:
                    continue

    # remove built ins
    libraries = stdlib_list("3.8")
    python_submodule.dependencies = set(all_imports) - set(libraries)

    packages_of_same_name, not_in_pypi = find_modules(
        list(python_submodule.dependencies), 250
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
                package_count+=1
            for bad_import in not_in_pypi:
                item = f"# {bad_import} # module imported but no package of same name\n"
                requirements.write(item)

    create_setup_py(package_folder, python_submodule)
    return file_to_write, package_count




def create_setup_py(package_folder: str, python_submodule: PythonPackage) -> None:
    """Just the setup.py part"""
    with open(
        package_folder + "/setup.py", "w", encoding="utf-8", errors="replace"
    ) as setup:
        data = {
            "package_name": python_submodule.package_name,
            "version": python_submodule.version,
            "url": python_submodule.url,
            "author": python_submodule.author,
            "author_email": python_submodule.author_email,
            "description": python_submodule.description,
            "dependencies": python_submodule.dependencies,
        }
        source = render_setup_py(data)
        setup.write(source)


def process_requirements_for_a_module(package_folder: str) -> None:
    """
    Call a commandline requirements generator
    """
    if settings.GENERATE_REQUIREMENTS_TXT:
        try:
            generate_requirements(package_folder)
        except subprocess.CalledProcessError as cpe:
            print(f"generate requirements failed : {package_folder}", str(cpe))
