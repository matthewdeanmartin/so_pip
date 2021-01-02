import so_pip.commands.freeze as freeze
import so_pip.commands.list_all as list_all
import so_pip.commands.show as show
from so_pip.utils.files_utils import find_file


def test_freeze():
    samples = find_file("../sample", __file__)
    freeze.freeze_environment(samples)


def test_list_all():
    samples = find_file("../sample", __file__)
    list_all.list_packages(samples)


def test_show():
    samples = find_file("../sample", __file__)
    show.show(samples, "find_imports_a_aboriginal_dig")
