"""
File writing stuff
"""
import os

import black
from black import format_str

from so_pip.settings import IGNORE_SYNTAX_ERRORS


def create_module_folder(target_folder, module_name) -> str:
    """Create folder and init file"""
    module_folder = f"{target_folder}/{module_name}"
    os.makedirs(module_folder, exist_ok=True)
    with open(f"{module_folder}/__init__.py", "w") as init_file:
        init_file.write("\n")
    return module_folder


def write_as_html(answer, submodule_name):
    """Dump answer is reasonable form."""
    with open(submodule_name + ".html", "w", encoding="utf-8") as diagnostics:
        diagnostics.write("<html><body>")
        diagnostics.write(answer.body)
        diagnostics.write("</body></html>")


def write_to_file(submodule_name, to_write):
    """format and dump it"""
    while to_write[-1].strip() in ("", "#"):
        to_write.pop()

    joined = "\n".join(to_write)

    with open(submodule_name, "w", encoding="utf-8") as generated:
        try:
            blackened = format_str(
                joined,
                mode=black.Mode(
                    target_versions={black.TargetVersion.PY38},
                    line_length=88,
                    string_normalization=True,
                    is_pyi=False,
                ),
            )
            generated.write(blackened)
        except Exception:
            if IGNORE_SYNTAX_ERRORS:
                generated.write(joined)
