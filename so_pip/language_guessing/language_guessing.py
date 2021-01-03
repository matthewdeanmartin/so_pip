"""
What programming language is this text
"""
from typing import List, Tuple

from so_pip.language_guessing.election import guess_language_all_methods
from so_pip.language_guessing.known_languages import FILE_EXTENSIONS
from so_pip.settings import DEFAULT_LANGUAGE

GUESS = None


def assign_extension(all_code: str, tags: List[str]) -> Tuple[str, str]:
    """Guess language and extension"""
    if not all_code:
        return DEFAULT_LANGUAGE

    result = guess_language_all_methods(code=all_code, tags=tags)
    if result:
        if result in FILE_EXTENSIONS:
            return FILE_EXTENSIONS[result], result
        return f".{result}", result

    return DEFAULT_LANGUAGE
