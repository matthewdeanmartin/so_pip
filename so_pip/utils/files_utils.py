"""
Just find file. Needs to be independent to avoid circular imports
"""
import os


def find_file(file_name: str, executing_file: str) -> str:
    """
    Create/find a valid file name relative to a source file, e.g.
    find_file("foo/bar.txt", __file__)
    """
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(executing_file)), file_name
    ).replace("\\", "/")
    return file_path
