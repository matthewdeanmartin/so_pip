from unittest.mock import patch

from so_pip.__main__ import process_docopts



def test_process_docopts():
    anything= {'--post': None,
 '--help': False,
 '--name': 'foo',
 '--package': None,
 '--question': None,
 '--vendor': '.',
 '--version': False,
 '<package>': [],
 'freeze': False,
 'list': True,
 'show': False,
 'uninstall': False,
 'vendorize': False}
    with patch("docopt.docopt", return_value=anything) as mock:
        process_docopts()
