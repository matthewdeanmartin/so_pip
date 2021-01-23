"""
Comment and write out anything
"""
from typing import List

from so_pip.support_files.generic_code_file import make_generic_code_file


def write_and_format_any_file(code_file_name: str, to_write: List[str]) -> bool:
    """format and dump it"""
    if "." not in code_file_name:
        raise TypeError("missing extension, likely")
    while to_write[-1].strip() == "":
        to_write.pop()

    joined = "\n".join(to_write)
    if not joined.strip():
        raise TypeError("Writing 0 bytes")
    make_generic_code_file(code_file_name, header="", code=joined, footer="")
    return True
