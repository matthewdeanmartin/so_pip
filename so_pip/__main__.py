"""so_pip/StackOverflow Pip
Not associated with PyPA, nor StackOverflow.

Usage:
  so_pip vendorize (--question=<question_id>|--answer=<answer_id>|--package=<package>)
  so_pip uninstall <package>...
  so_pip list
  so_pip freeze
  so_pip show <package>...
  so_pip (-h | --help)
  so_pip --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --output      Folder for packages.

"""
from docopt import docopt

import so_pip._version as meta
import so_pip.commands.vendorize as vendorize
import so_pip.commands.list_all as list_all
import so_pip.commands.uninstall as uninstall
import so_pip.commands.show as show
from so_pip.settings import TARGET_FOLDER


def process_docopts():
    """Get the args object from command parameters"""
    arguments = docopt(__doc__, version=f'so_pip {meta.__version__}')
    # print(arguments)

    # example
    # arguments = {'--answer': None,
    #            '--help': False,
    #            '--package': '123',
    #            '--question': None,
    #            '--version': False,
    #            '<package>': [],
    #            'freeze': False,
    #            'list': False,
    #            'show': False,
    #            'uninstall': False,
    #            'vendorize': True}
    target_folder = TARGET_FOLDER
    if arguments["vendorize"]:
        question = arguments["--question"]
        packages_made = vendorize.import_so(f"q{question}", question)
        print(f"Vendorized {','.join(packages_made)} at {target_folder}")
    if arguments["uninstall"]:
        packages = arguments["<package>"]
        for package in packages:
            uninstall.uninstall_package(target_folder, package)
        print(f"Uninstalled {','.join(packages)} from vendorized folder.\n"
              f"If you also installed with pip you will need to uninstall with pip")
    if arguments["list"]:
        list_all.list_packages(target_folder)
    if arguments["show"]:
        packages = arguments["<package>"]
        for package in packages:
            show.show(target_folder, package)

if __name__ == '__main__':
    process_docopts()
