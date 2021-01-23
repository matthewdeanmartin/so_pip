"""
SO questions and answers look a lot alike jupyter notebooks.
"""
import json
from typing import Any, Dict

import nbformat

from so_pip.models.python_package_model import CodePackage
from so_pip.parse_python.format_code import deindent


def write_jupyter_notebook(
    post: Dict[str, Any], package_info: CodePackage, submodule_path: str
) -> None:
    """75% of SO answers are written in the form of a notebook."""

    # TODO: jupyter supports 100+ kernels
    #  https://github.com/jupyter/jupyter/wiki/Jupyter-kernels

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

    markdown_lines = []
    code = []
    state = "md"
    normal_markdown = post["body_markdown"].replace("\r\n", "\n").replace("\r", "\n")
    for line in normal_markdown.split("\n"):
        # could be either.
        if not line.strip():
            if markdown_lines or state == "md":
                markdown_lines.append(line)
                continue
            if code or state == "code":
                code.append(line)
                continue

        # now in code.
        if line.startswith("    "):
            # change over
            if markdown_lines:
                cell = nbformat.v4.new_markdown_cell(source="\n".join(markdown_lines))
                notebook.cells.append(cell)
                markdown_lines = []
            code.append(line)
            state == "code"
            continue

        # now in markdown
        if code:
            cell = nbformat.v4.new_code_cell(source=deindent("\n".join(code)))
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

    with open(f"{submodule_path}.ipynb", "w", encoding="utf-8") as file:
        string = json.dumps(notebook)
        file.write(string)
