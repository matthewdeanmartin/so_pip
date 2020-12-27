"""so_pip/StackOverflow Pip
Not associated with PyPA, nor StackOverflow.

Usage:
  so_pip vendorize --name=<name> (--question=<question_id>|--answer=<answer_id>|--package=<package>) [--vendor=<vendor>]
  so_pip uninstall <package>...   [--vendor=<vendor>]
  so_pip list   [--vendor=<vendor>]
  so_pip freeze   [--vendor=<vendor>]
  so_pip show <package>...   [--vendor=<vendor>]
  so_pip (-h | --help)
  so_pip --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --vendor=<vendor>      Folder for packages.
  --question=<question_id>    Stackoverflow question id
  --answer=<answer_id>      Stackoverflow answer id
  --package=<package>     Generated package name


"""
import docopt

from so_pip import _version as meta
from so_pip import settings as settings
from so_pip.commands import list_all as list_all
from so_pip.commands import show as show
from so_pip.commands import uninstall as uninstall
from so_pip.commands import vendorize as vendorize


def process_docopts() -> None:
    """Get the args object from command parameters"""
    arguments = docopt.docopt(__doc__, version=f"so_pip {meta.__version__}")
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
    print(arguments)
    target_folder = arguments["--vendor"]
    if target_folder:
        settings.TARGET_FOLDER = target_folder
    else:
        settings.TARGET_FOLDER = "../output"
    if arguments["vendorize"]:
        prefix = arguments["--name"]
        question = arguments["--question"]
        answer = arguments["--answer"]
        if question:
            packages_made = vendorize.import_so_question(prefix, question)
        if answer:
            packages_made = vendorize.import_so_answer(prefix, answer)
        print(f"Vendorized {','.join(packages_made)} at {target_folder}")
    if arguments["uninstall"]:
        packages = arguments["<package>"]
        for package in packages:
            uninstall.uninstall_package(target_folder, package)
        print(
            f"Uninstalled {','.join(packages)} from vendorized folder.\n"
            f"If you also installed with pip you will need to uninstall with pip"
        )
    if arguments["list"]:
        list_all.list_packages(target_folder)
    if arguments["show"]:
        packages = arguments["<package>"]
        for package in packages:
            show.show(target_folder, package)


if __name__ == "__main__":
    process_docopts()
