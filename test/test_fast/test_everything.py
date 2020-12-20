import so_pip._version

def test_import_it():
    # lamest, first test.
    import so_pip
    dir(so_pip)
    assert so_pip._version.__version__
    #
    # import so_pip.create_requirements_txt
    # import so_pip.external_commands
    import so_pip.main
    dir(so_pip.main)
    # import so_pip.transformations
