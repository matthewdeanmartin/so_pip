from unittest.mock import patch

from so_pip.__main__ import process_docopts
from so_pip.utils.files_utils import find_file


def test_process_docopts():
    anything= {'--post': '2572654',
 '--help': False,
 '--name': 'foo',
 '--package': None,
 '--question': None,
 '--vendor': find_file('../../output/unit_tests/', __file__),
 '--version': False,
 '<package>': [],
 'freeze': False,
 'list': False,
 'show': False,
 'uninstall': False,
 'vendorize': True}
    with patch("docopt.docopt", return_value=anything) as mock:
        process_docopts()
