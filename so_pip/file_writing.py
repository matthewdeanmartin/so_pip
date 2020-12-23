"""
File writing stuff
"""
import os
import shutil
from typing import List, Union

import black
import stackexchange
from black import format_str

from so_pip.settings import IGNORE_SYNTAX_ERRORS


def find_file(file_name: str, executing_file: str) -> str:
    """
    Create/find a valid file name relative to a source file, e.g.
    find_file("foo/bar.txt", __file__)
    """
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(executing_file)), file_name
    ).replace("\\", "/")
    return file_path


def write_license(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_folder: str
) -> None:
    """Include license file
    Each revision could have different license!
    """
    license_name = post.json.get("content_license", "N/A")
    if license_name == "N/A":
        print(post.json)
        return
    license_path = find_file(f"licenses/{license_name}.txt", __file__)
    destination_path = find_file(f"{submodule_folder}/LICENSE", __file__)

    shutil.copy(license_path, destination_path)


def write_as_html(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_name
) -> None:
    """Dump answer in readable form."""
    with open(submodule_name + ".html", "w", encoding="utf-8") as diagnostics:
        diagnostics.write("<html><body>")
        diagnostics.write(post.body)
        diagnostics.write("</body></html>")


def write_as_md(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_name
) -> None:
    """Dump post in readable form."""
    try:
        markdown = post.body_markdown
        with open(submodule_name + ".md", "w", encoding="utf-8") as diagnostics:
            diagnostics.write(markdown)
    except Exception as ex:
        print(ex)


def write_and_format_python_file(submodule_name: str, to_write: List[str]) -> bool:
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
            return True
        except black.InvalidInput:
            if IGNORE_SYNTAX_ERRORS:
                generated.write(joined)
                return True
    return False
