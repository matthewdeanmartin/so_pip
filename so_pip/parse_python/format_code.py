"""
Format and save python.
"""
import textwrap

import black
from black import format_str


def format_python_file(code: str) -> str:
    """format and dump it"""
    try:
        blackened = format_str(
            code,
            mode=black.Mode(
                target_versions={black.TargetVersion.PY38},
                line_length=88,
                string_normalization=True,
                is_pyi=False,
            ),
        )
        if not blackened:
            raise TypeError("Writing 0 bytes")
        return blackened
    except black.InvalidInput:
        # TODO: if settings.COMMENT_OUT_BAD_PYTHON:
        return code


def deindent(code: str) -> str:
    """Remove leading whitespace"""
    return textwrap.dedent(code)
