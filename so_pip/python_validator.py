"""
Is this valid python, what version?

Valid syntax is valid.
Invalid syntax could still be python
Invalid syntax could also be something that isn't python at all.
"""
import ast
import subprocess  # nosec
from typing import List, Tuple

from so_pip.external_commands import pyflakes


def validate_python(code: str) -> Tuple[bool, List[str]]:
    """Validate by ast parsing"""
    try:
        _ = ast.parse(code)
        # same, but also writes files, I think
        # __ = compile(code, 'blah.py', 'exec', dont_inherit=True)
        return True, []
    except SyntaxError as syntax_error:
        error_message = f"{str(syntax_error)}"
    return False, [error_message]


def validate_with_pyflakes(file_name: str) -> Tuple[bool, List[str]]:
    """Does pyflakes think this is valid python?"""
    # pyflakes doesn't recognize latest versions of py3.x
    try:
        results = pyflakes(file_name)
        if "syntax" in results:
            return False, results.split("/")
    except subprocess.CalledProcessError as cpe:
        return False, [str(cpe)]
    return True, []
