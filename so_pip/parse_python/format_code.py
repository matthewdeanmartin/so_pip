"""
Format and save python.
"""
import textwrap
from typing import List

import black
from black import format_str

from so_pip import settings as settings


def write_and_format_python_file(file_name: str, to_write: List[str]) -> bool:
    """format and dump it"""
    if not file_name.endswith(".py"):
        raise TypeError("Why don't we have a .py extension?")

    while to_write[-1].strip() in ("", "#"):
        to_write.pop()

    joined = "\n".join(to_write)

    with open(file_name, "w", encoding="utf-8") as generated:
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
            if settings.COMMENT_OUT_BAD_PYTHON:
                generated.write(joined)
                return True
    return False


def deindent(code: str) -> str:
    """Remove leading whitespace"""
    return textwrap.dedent(code)
