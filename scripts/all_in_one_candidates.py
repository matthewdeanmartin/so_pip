from so_pip.commands.vendorize import import_so_question, import_so_answer
from so_pip.utils.files_utils import find_file

OUTPUT_FOLDER = find_file("../output", __file__)
if __name__ == "__main__":
    # https://stackoverflow.com/questions/29312494/

    # import_so_question("lua", 29312494, OUTPUT_FOLDER)
    # https://stackoverflow.com/questions/32833797/

    # https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    import_so_question("encrypt", 12524994, OUTPUT_FOLDER)
