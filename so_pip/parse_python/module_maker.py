"""
Generate all the python related files for a module
- folder
- each post
- sort imports
"""
import logging
import os
from typing import Any, Dict, List, Tuple

from so_pip import settings as settings
from so_pip.cli_clients.external_commands import isort
from so_pip.models.code_block_from_text import find_code_blocks
from so_pip.models.code_file_model import CodeFile
from so_pip.models.python_package_model import CodePackage
from so_pip.parse_python.upgrade_to_py3 import upgrade_string
from so_pip.settings import CODE_IN_SRC_FOLDER, PYTHON_CODE_IN_MODULE_FOLDER
from so_pip.support_files.python_init import make_python_init_file

LOGGER = logging.getLogger(__name__)


def create_package_folder(
    target_folder: str, package_name: str, module_name: str, code_info: CodePackage
) -> Tuple[str, str]:
    """Create folder and init file"""
    source_folder = "/SRC/" if CODE_IN_SRC_FOLDER else "/"
    is_python = any(_.language == "python" for _ in code_info.code_blocks)

    # python needs that folder & __init__.py, otherwise you get n modules per package
    # a my_package/my_folder structure lets you add many files & still have
    # just one module name to mention in the pyproject.toml
    if PYTHON_CODE_IN_MODULE_FOLDER and is_python:
        # e.g. output/my_package/my_module
        # and  output/my_package/my_module/__init__.py
        # and  output/my_package/my_module/main.py
        supporting_files_folder = f"{target_folder}{source_folder}{package_name}/"
        python_source_folder = (
            f"{target_folder}{source_folder}{package_name}/" f"{module_name}"
        )
    else:
        # e.g. output/my_package/
        # and  no __init__.py !
        # and  output/my_package/main.py
        supporting_files_folder = f"{target_folder}/{package_name}/"
        python_source_folder = f"{target_folder}/{package_name}"

    os.makedirs(python_source_folder, exist_ok=True)

    # this will skip if there are no python files
    if PYTHON_CODE_IN_MODULE_FOLDER:
        make_python_init_file(
            file_name=f"{python_source_folder}/__init__.py", code_info=code_info
        )

    return supporting_files_folder, python_source_folder


def map_post_to_code_package_model(
    post: Dict[str, Any], html: str, name: str, description: str, tags: List[str]
) -> CodePackage:
    """Given html of ap post, fill in a CodePackage object."""
    package = CodePackage(package_name=name, description=description)
    package.extract_metadata(post=post)
    package.code_blocks.extend(find_code_blocks(html, tags))
    if not package.code_blocks:
        raise TypeError("Expected some code blocks by now")
    first = True
    for block in package.code_blocks:
        if block.starts_new_file or len(package.code_blocks) == 1 or first:
            code_file = CodeFile()
            package.code_files.append(code_file)
            first = False
        code_file.code_blocks.append(block)
        code = block.code_text
        if settings.ASSUME_ONE_LINER_IS_NOT_CODE and "\n" not in block.code_text:
            LOGGER.debug("Skipping this because it is just one line:")
            LOGGER.debug(code)
        if block.extension == ".py" and settings.BUMP_TO_PY3:
            block.code_text = upgrade_string(block.code_text)
        # commenting done in the to_write() method

    for code_file in package.code_files:
        if not code_file.extension:
            code_file.analyze(tags)
        if not code_file.extension:
            raise TypeError("Expected Extension by now")
    return package


def isort_a_module(module_folder: str) -> None:
    """Just call isort."""
    isort(module_folder)
