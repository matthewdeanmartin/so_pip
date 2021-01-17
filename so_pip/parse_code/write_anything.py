"""
Comment and write out anything
"""
from typing import List


def write_and_format_any_file(code_file_name: str, to_write: List[str]) -> bool:
    """format and dump it"""
    if "." not in code_file_name:
        raise TypeError("missing extension, likely")
    while to_write[-1].strip() == "":
        to_write.pop()

    joined = "\n".join(to_write)

    with open(code_file_name, "w", encoding="utf-8") as generated:
        if not joined.strip():
            raise TypeError("Writing 0 bytes")
        generated.write(joined)
    return True
