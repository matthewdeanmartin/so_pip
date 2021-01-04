from so_pip.commands.vendorize import import_so_answer, import_so_question
from so_pip.utils.files_utils import find_file

OUTPUT_FOLDER = find_file("../../output", __file__)


def test_import_so():
    # # https://stackoverflow.com/questions/9008451/python-easy-way-to-read-all-import-statements-from-py-module
    # import_so_question("find_imports_better", 9008451)
    # import_so_question("question_matters", 65373654)
    # # https://stackoverflow.com/questions/2572582/return-a-list-of-imported-python-modules-used-in-a-script
    import_so_question("find_imports", 2572582, OUTPUT_FOLDER)
    # # has fiddle, strong evidence of working code
    # # https://stackoverflow.com/questions/5874652/prop-vs-attr
    # 24139250
    # import_so("pyso_answers_by_user", 24139250)


def test_import_so_answer():
    import_so_answer("test", 2572654, OUTPUT_FOLDER, None)


def test_handle_answer_escape_in_source():
    import_so_answer("escape", 64476551, OUTPUT_FOLDER, None)


def test_answer_missing_last_code_block():
    import_so_answer("missing_cb", 22489076, OUTPUT_FOLDER, None)
