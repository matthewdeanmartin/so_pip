"""
Generate all the python related files for a module
- folder
- each answer
- sort imports
"""
import os

from so_pip.cli_clients.external_commands import isort
from so_pip.model import CodeFile, PythonSubmodule
from so_pip.parse_code.arbitrary_code_block import find_code_blocks
from so_pip.parse_python.code_transformations import html_to_python_comments
from so_pip.parse_python.upgrade_to_py3 import upgrade_string
from so_pip.settings import ASSUME_ONE_LINER_IS_NOT_CODE


def create_module_folder(target_folder: str, module_name: str, metadata: str) -> str:
    """Create folder and init file"""
    module_folder = f"{target_folder}/{module_name}"
    os.makedirs(module_folder, exist_ok=True)
    with open(f"{module_folder}/__init__.py", "w") as init_file:
        if metadata:
            init_file.write(metadata)
        else:
            init_file.write("\n")

    return module_folder


def handle_python_post(html: str, name: str, description: str) -> PythonSubmodule:
    """Build up lines to write as list."""
    submodule = PythonSubmodule(package_name=name, description=description)
    submodule.code_blocks.extend(find_code_blocks(html))
    if not submodule.code_blocks:
        raise TypeError("Expected some code blocks by now")
    first = True
    for block in submodule.code_blocks:
        if block.starts_new_file or len(submodule.code_blocks) == 1 or first:
            code_file = CodeFile()
            submodule.code_files.append(code_file)
            first = False
        code_file.code_blocks.append(block)
        code = block.code_text
        if ASSUME_ONE_LINER_IS_NOT_CODE and "\n" not in block.code_text:
            print(code)
        if block.extension == ".py":
            block.code_text = upgrade_string(block.code_text)
            # comment out bad py code here.
            block.header_comments = html_to_python_comments(block.header_comments)
            block.footer_comments = html_to_python_comments(block.footer_comments)
    for code_file in submodule.code_files:
        if not code_file.extension:
            code_file.analyze()
        if not code_file.extension:
            raise TypeError("Expected Extension by now")

        # if block.is_valid_python:
        #     code_file.to_write.append(code)
        #     code_file.all_code.append(code)
        # else:
        #     submodule.failed_parse = True
        #     if COMMENT_OUT_BAD_PYTHON and block.extension == ".py":
        #         commented_out_code = html_to_python_comments(code)
        #         for error in block.errors:
        #
        #             error_message = f"# Syntax error: {error}"
        #             code_file.to_write.append("# " + error_message)
        #         code_file.to_write.append(commented_out_code)
        #
        # if block.footer_comments:
        #     code_file.to_write.append(block.footer_comments)
        #
        # code_file.strip_trailing_blank()
    return submodule


def isort_a_module(module_folder: str) -> None:
    """Just call isort."""
    isort(module_folder)
