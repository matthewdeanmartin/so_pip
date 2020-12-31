from so_pip.commands.vendorize import import_so_question, import_so_answer


def test_import_so():
    # # https://stackoverflow.com/questions/9008451/python-easy-way-to-read-all-import-statements-from-py-module
    import_so_question("find_imports_better", 9008451)
    import_so_question("question_matters", 65373654)
    # # https://stackoverflow.com/questions/2572582/return-a-list-of-imported-python-modules-used-in-a-script
    import_so_question("find_imports", 2572582)
    # # has fiddle, strong evidence of working code
    # # https://stackoverflow.com/questions/5874652/prop-vs-attr
    # 24139250
    #import_so("pyso_answers_by_user", 24139250)

def test_import_so_answer():
    import_so_answer("test", 2572654)

def test_handle_answer_escape_in_source():
    import_so_answer("escape", 64476551)

def test_answer_missing_last_code_block():
    import_so_answer("missing_cb", 22489076)
