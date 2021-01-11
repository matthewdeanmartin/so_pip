"""
Is this valid python, what version?

Valid syntax is valid.
Invalid syntax could still be python
Invalid syntax could also be something that isn't python at all.
"""
import ast
import subprocess  # nosec
from typing import List, Tuple

from so_pip.cli_clients.external_commands import pyflakes, vermin


def validate_with_vermin(folder: str) -> str:
    """Infer python versions"""
    result = vermin(folder)
    # "Minimum required versions: 2.0  Incompatible versions:     3"
    # ~2       No known reason it won't work with py2.
    # !2       It is known that it won't work with py2.
    # 2.5, !3  Works with 2.5+ but it is known it won't work with py3.
    # ~2, 3.4  No known reason it won't work with py2, works with 3.4+"
    # print(result)
    if "~2, ~3" in result:
        return "*"
    if "2.0, 3.0" in result:
        return "*"
    # pylint: disable=broad-except
    # noinspection PyBroadException
    try:
        parts = result.split(":")
        minimum = parts[1].strip().split(" ")[0].strip("\n")
        if "\n" in minimum:
            minimum = minimum.split("\n")[0]
        if "," in minimum:
            minimum = minimum.split(",")
        if "Incompatible" in result:
            parts = result.split("Incompatible versions:")
            maximum = parts[1].strip("\n").strip(" ")
            maximum = f"!{maximum}"
        else:
            maximum = ""
    except BaseException:
        print("unexpected compat string")
        print(result)
        raise
    if maximum:
        return f">={minimum}, {maximum}"
    return f">={minimum}"


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
