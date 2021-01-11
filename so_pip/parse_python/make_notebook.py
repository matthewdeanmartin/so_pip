"""
SO questions and answers look a lot alike jupyter notebooks.
"""
import json

import nbformat


def proof_of_concept() -> None:
    """This is not ready for prime time."""
    thing = nbformat.v4.new_notebook()

    cell = nbformat.v4.new_code_cell(source="print('hello')")
    md_cell = nbformat.v4.new_markdown_cell(
        source="""Things are looking up
    --------
    _are_ *they* not?
    """,
    )
    thing.metadata = {
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

    thing.cells = [cell, md_cell]
    with open("thing.ipynb", "w", encoding="utf-8") as file:
        string = json.dumps(thing)
        file.write(string)
