from so_pip.pypi_query.main import PackageInfo


def test_do_they_exist():
    p = PackageInfo()
    assert p.search("str")
    assert not p.search("bool")
