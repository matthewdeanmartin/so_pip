"""
SO questions and answers look a lot alike jupyter notebooks.
"""
import html
import json
from typing import Any, Dict, List

import nbformat
from nbformat import NotebookNode

from so_pip.models.python_package_model import CodePackage
from so_pip.parse_python.code_transformations import fix_interactive
from so_pip.parse_python.format_code import deindent


def write_jupyter_notebook(
    post: Dict[str, Any], code_info: CodePackage, submodule_path: str
) -> bool:
    """75% of SO answers are written in the form of a notebook."""

    # TODO: jupyter supports 100+ kernels
    #  https://github.com/jupyter/jupyter/wiki/Jupyter-kernels
    has_python = any(_.language == "python" for _ in code_info.code_blocks)
    if not has_python:
        return False
    notebook = parse_to_jupyter_notebook(post["body_markdown"])
    with open(f"{submodule_path}.ipynb", "w", encoding="utf-8") as file:
        string = json.dumps(notebook)
        file.write(string)
    return True


def parse_to_jupyter_notebook(body_markdown: str) -> NotebookNode:
    """
    Just turn markdown into a notebook
    """
    # TODO: check python version and set python 2/3 correctly
    notebook = nbformat.v4.new_notebook()
    notebook.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 2},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython2",
            "version": "2.7.6",
        },
    }

    markdown_lines: List[str] = []
    code: List[str] = []
    state = "md"
    normal_markdown = body_markdown.replace("\r\n", "\n").replace("\r", "\n")
    for line in normal_markdown.split("\n"):
        # could be either.
        if not line.strip() and state != "code":
            if markdown_lines or state == "md":
                # BUG: lines in code don't start with four spaces.
                if line:
                    markdown_lines.append(line)
                continue
            if code or state == "code":
                code.append(line)
                continue

        # now in code.
        if line.startswith("    ") or line == "":
            # change over
            if markdown_lines and not all(_ == "" for _ in markdown_lines):
                cell = nbformat.v4.new_markdown_cell(source="\n".join(markdown_lines))
                notebook.cells.append(cell)
                markdown_lines = []
            code.append(line)
            state = "code"
            continue

        # now in markdown
        if code:
            source = deindent(html.unescape("\n".join(code)))
            source = fix_interactive(source)
            if "&gt;" in source:
                raise TypeError("unescape failed")
            cell = nbformat.v4.new_code_cell(source=source)
            notebook.cells.append(cell)
            code = []
        markdown_lines.append(line)
        state = "md"

    if markdown_lines:
        cell = nbformat.v4.new_markdown_cell(source="\n".join(markdown_lines))
        notebook.cells.append(cell)
    if code:
        cell = nbformat.v4.new_code_cell(source=deindent("\n".join(code)))
        notebook.cells.append(cell)
    return notebook
