from unittest.mock import patch

from so_pip.__main__ import process_docopts



def test_process_docopts():
    anything= {'--post': '2572654',
 '--help': False,
 '--name': 'foo',
 '--package': None,
 '--question': None,
 '--vendor': 'so_pip_packages',
 '--version': False,
 '<package>': [],
 'freeze': False,
 'list': False,
 'show': False,
 'uninstall': False,
 'vendorize': True}
    with patch("docopt.docopt", return_value=anything) as mock:
        process_docopts()
