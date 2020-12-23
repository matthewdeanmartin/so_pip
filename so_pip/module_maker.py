"""
Generate all the python related files for a module
- folder
- each answer
- sort imports
"""
import os

import stackexchange
from bs4 import BeautifulSoup

from so_pip.code_transformations import (
    fix_interactive,
    fix_shell,
    html_to_python_comments,
)
from so_pip.external_commands import isort
from so_pip.model import PythonSubmodule
from so_pip.python_validator import validate_python
from so_pip.settings import ASSUME_ONE_LINER_IS_NOT_CODE, IGNORE_SYNTAX_ERRORS
from so_pip.upgrade_to_py3 import upgrade_string


def create_module_folder(target_folder: str, module_name: str) -> str:
    """Create folder and init file"""
    module_folder = f"{target_folder}/{module_name}"
    os.makedirs(module_folder, exist_ok=True)
    with open(f"{module_folder}/__init__.py", "w") as init_file:
        init_file.write("\n")
    return module_folder


def handle_python_answer(html: str, name: str, description: str) -> PythonSubmodule:
    """Build up lines to write as list."""
    submodule = PythonSubmodule(package_name=name, description=description)

    regex_expression = '(<pre class="[a-z -]*"><code>|<pre><code>|</code></pre>)'
    parts = stackexchange.re.split(regex_expression, html)

    in_comment = True
    for part in parts:
        if part.startswith("<pre") and part.endswith("<code>"):
            in_comment = False
            continue
        if part == "</code></pre>":
            in_comment = True
            continue
        if in_comment:
            comment = html_to_python_comments(part)
            if comment:
                submodule.to_write.append(comment)
            # not in comment anymore, remove blank lines.
            submodule.strip_trailing_blank()
            continue

        # handle html escapes in what is mostly not html
        soup = BeautifulSoup(
            "<pre><code>" + part + "</code></pre>", features="html.parser"
        )
        code = soup.findAll("code")[0].text

        if ASSUME_ONE_LINER_IS_NOT_CODE and "\n" not in code:
            print(code)
            continue

        code = fix_interactive(code)
        code = fix_shell(code)
        code = upgrade_string(code)

        python_is_valid, errors = validate_python(code)
        if python_is_valid:
            submodule.to_write.append(code)
            submodule.all_code.append(code)
        else:
            submodule.failed_parse = True
            if IGNORE_SYNTAX_ERRORS:
                for error in errors:
                    error_message = f"# Syntax error: {error}"
                    submodule.to_write.append(error_message)
                submodule.to_write.append(code)
                submodule.all_code.append(code)

    submodule.strip_trailing_blank()
    return submodule


def isort_a_module(module_folder: str) -> None:
    """Just call isort."""
    isort(module_folder)
