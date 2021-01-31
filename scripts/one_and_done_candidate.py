"""
Good examples of one-and-done. An answer so re-usable it could be a pypi package.
"""

from so_pip.commands.vendorize import import_so_question, import_so_answer
from so_pip.utils.files_utils import find_file

OUTPUT_FOLDER = find_file("../output", __file__)
if __name__ == "__main__":
    # https://stackoverflow.com/a/38187562/33264
    # 38187562
    import_so_answer("halversine", 38187562, OUTPUT_FOLDER, revision_id=None)
