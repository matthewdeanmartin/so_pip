from unittest.mock import patch

from so_pip.__main__ import main
from so_pip.utils.files_utils import find_file


def test_process_docopts():
    anything = {
        "--count": "2",
        "--help": False,
        "--output": find_file("../../output/unit_tests/", __file__),
        "--package": None,
        "--post": "2572654",
        "--query": "how to write code",
        "--question": None,
        "--tags": "python",
        "--vendor": None,
        "--version": False,
        "<name>": "abc",
        "<names>": [],
        "freeze": False,
        "list": False,
        "search": False,
        "show": False,
        "uninstall": False,
        "vendorize": True,
    }
    with patch("docopt.docopt", return_value=anything) as mock:
        main()


def test_process_docopts_other():
    anything = {
        "--count": "2",
        "--help": False,
        "--output": find_file("../../output/unit_tests/", __file__),
        "--package": None,
        "--post": "2572654",
        "--query": "how to write code",
        "--question": None,
        "--tags": "python",
        "--vendor": None,
        "--version": False,
        "<name>": "abc",
        "<names>": [],
        "freeze": False,
        "list": False,
        "search": False,
        "show": False,
        "uninstall": False,
        "vendorize": True,
    }
    with patch("docopt.docopt", return_value=anything) as mock:
        assert main() == 0
