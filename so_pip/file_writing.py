"""
File writing stuff
"""
import os
from typing import Union

import stackexchange


def find_file(file_name: str, executing_file: str) -> str:
    """
    Create/find a valid file name relative to a source file, e.g.
    find_file("foo/bar.txt", __file__)
    """
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(executing_file)), file_name
    ).replace("\\", "/")
    return file_path


def write_as_html(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_name: str
) -> None:
    """Dump answer in readable form."""
    with open(submodule_name + ".html", "w", encoding="utf-8") as diagnostics:
        diagnostics.write("<html><body>")
        diagnostics.write(post.body)
        diagnostics.write("</body></html>")


def write_as_md(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_name: str
) -> None:
    """Dump post in readable form."""
    try:
        markdown = post.body_markdown
    except AttributeError as attribute_error:
        print(attribute_error)
        return
    with open(submodule_name + ".md", "w", encoding="utf-8") as diagnostics:
        diagnostics.write(markdown)
