from so_pip.infer_packages_needed.package_by_name import PackageInfo


def test_do_they_exist():
    p = PackageInfo()
    assert p.search("str")
    assert not p.search("bool")
