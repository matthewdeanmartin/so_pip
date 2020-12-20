from so_pip.main import import_so


def test_import_so():
    import_so("question_matters", 65373654)
    # https://stackoverflow.com/questions/2572582/return-a-list-of-imported-python-modules-used-in-a-script
    import_so("find_imports", 2572582)
    # has fiddle, strong evidence of working code
    # https://stackoverflow.com/questions/5874652/prop-vs-attr
