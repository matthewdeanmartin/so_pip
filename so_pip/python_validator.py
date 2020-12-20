"""
Is this valid python, what version?
"""
import ast
from typing import List, Tuple


def validate_python(code: str) -> Tuple[bool, List[str]]:
    try:
        _ = ast.parse(code)
        # same thing?
        # __ = compile(code, 'blah.py', 'exec', dont_inherit=True)
        return True, []
    except SyntaxError as syntax_error:
        error_message = f"{str(syntax_error)}"
    return False, [error_message]
