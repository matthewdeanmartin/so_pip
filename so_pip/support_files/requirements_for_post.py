"""
Using source code, find requirements
"""
import os
import subprocess  # nosec

from stdlib_list import stdlib_list

from so_pip.api_clients.pypstats_facade import find_modules

# ^\s*(from|import)\s+\w+
from so_pip.cli_clients.external_commands import generate_requirements
from so_pip.models.python_package_model import PythonPackage
from so_pip.settings import GENERATE_REQUIREMENTS_TXT
from so_pip.support_files.setup_py import render_setup_py
from so_pip_packages.find_imports import main as find_imports

# https://github.com/ohjeah/pip-validate


def requirements_for_file(module_folder: str, python_submodule: PythonPackage) -> None:
    """Requirements for running `safety`"""
    all_imports = []
    for filename in os.listdir(module_folder):
        if filename.endswith(".py"):
            py_file = os.path.join(module_folder, filename)
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
        with open(
            module_folder + "/requirements.txt", "w", encoding="utf-8", errors="replace"
        ) as requirements:
            requirements.write("# module names often don't match package names!\n\n")
            for _import in packages_of_same_name:
                requirements.write(_import + "\n")
            for bad_import in not_in_pypi:
                item = f"# {bad_import} # module imported but no package of same name\n"
                requirements.write(item)

    with open(
        module_folder + "/setup.py", "w", encoding="utf-8", errors="replace"
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


def process_requirements_for_a_module(module_folder: str) -> None:
    """
    Call a commandline requirements generator
    """
    if GENERATE_REQUIREMENTS_TXT:
        try:
            generate_requirements(module_folder)
        except subprocess.CalledProcessError as cpe:
            print(f"generate requirements failed : {module_folder}", str(cpe))
