"""
Examples of questions where there are lots of good alternates & they
should all be in one library.
"""

from so_pip.commands.vendorize import import_so_question, import_so_answer
from so_pip.utils.files_utils import find_file

OUTPUT_FOLDER = find_file("../output", __file__)
if __name__ == "__main__":
    # https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    import_so_question("encrypt", 12524994, OUTPUT_FOLDER, all_in_one=True)
