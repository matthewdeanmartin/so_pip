from so_pip.parse_python.make_notebook import parse_to_jupyter_notebook
from so_pip.utils.files_utils import find_file


def test_simple_nb():
    sample = find_file("post.md", __file__)
    sample_md = open(sample).read()
    result = parse_to_jupyter_notebook(sample_md)
    for j, k in result.items():
        if j == "cells":
            for cell in k:
                if (
                    cell.get("cell_type", "Nope") == "markdown"
                    and cell.get("source", "No Source") == ""
                ):
                    raise TypeError("Invalid")
                print(cell)
