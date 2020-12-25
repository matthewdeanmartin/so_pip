from so_pip.commands.vendorize import import_so


def test_import_so():
    # # https://stackoverflow.com/questions/9008451/python-easy-way-to-read-all-import-statements-from-py-module
    import_so("find_imports_better",9008451)
    import_so("question_matters",  65373654)
    # # https://stackoverflow.com/questions/2572582/return-a-list-of-imported-python-modules-used-in-a-script
    import_so("find_imports", 2572582)
    # # has fiddle, strong evidence of working code
    # # https://stackoverflow.com/questions/5874652/prop-vs-attr
    # 24139250
    #import_so("pyso_answers_by_user", 24139250)
