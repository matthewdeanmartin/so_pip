# noinspection PyPep8
"""so_pip/StackOverflow Pip
Not associated with PyPA, nor StackOverflow.

Usage:
  so_pip vendorize <name> (--question=<question_id>|--post=<answer_id>|--package=<package>) [--output=<output>] [--logs]
  so_pip search <name> --query=<query> --tags=<tags> [--output=<output>] [--count=<count>] [--logs]
  so_pip uninstall <names>...   [--output=<output>] [--logs]
  so_pip list   [--output=<output>] [--logs]
  so_pip freeze   [--output=<output>] [--logs]
  so_pip show <names>...   [--vendor=<output>] [--logs]
  so_pip (-h | --help)
  so_pip --version

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  --count=<count>           How many posts to get [default: 2].
  --output=<output>         Folder for packages. Defaults to /output
  --question=<question_id>  Stackoverflow question id
  --post=<answer_id>        Stackoverflow post id
  --package=<package>       Generated package name
  --logs                    Show logging

"""
import logging

import sys

import docopt

from so_pip import _version as meta
from so_pip.commands import freeze as freeze
from so_pip.commands import list_all as list_all
from so_pip.commands import search as search
from so_pip.commands import show as show
from so_pip.commands import uninstall as uninstall
from so_pip.commands import vendorize as vendorize


def main() -> int:
    """Get the args object from command parameters"""
    arguments = docopt.docopt(__doc__, version=f"so_pip {meta.__version__}")
    # print(arguments)
    output_folder = arguments["--output"]

    if arguments["--logs"]:
        # root logger, all modules
        for root in ("so_pip", "__main__", "url_lib3"):
            logger = logging.getLogger(root)
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            formatter = logging.Formatter(log_format)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
    if arguments["vendorize"]:
        prefix = arguments["<name>"]
        question = arguments["--question"]
        answer = arguments["--post"]
        if question:
            packages_made = vendorize.import_so_question(
                prefix, question, output_folder
            )
        elif answer:
            packages_made = vendorize.import_so_answer(prefix, answer, output_folder)
        else:
            raise TypeError("Need to specify a question or answer")
        print(f"Vendorized {','.join(packages_made)} at {output_folder}")
    elif arguments["uninstall"]:
        packages = arguments["<name>"]
        for package in packages:
            uninstall.uninstall_package(output_folder, package)
        print(
            f"Uninstalled {','.join(packages)} from vendorized folder.\n"
            f"If you also installed with pip you will need to uninstall with pip"
        )
    elif arguments["list"]:
        list_all.list_packages(output_folder)
    elif arguments["freeze"]:
        freeze.freeze_environment(output_folder)
    elif arguments["show"]:
        packages = arguments["<names>"]
        for package in packages:
            show.show(output_folder, package)
    elif arguments["search"]:
        prefix = arguments["<name>"]
        query = arguments["--query"]
        try:
            count_str = arguments["--count"]
            count = int(count_str)
        except ValueError:
            print(f"Can't convert {count_str} to a number")
            return -1

        # TODO: better way to do this with docopts
        if arguments["--tags"]:
            tags = arguments["--tags"].split(";,")
        else:
            tags = []
        search.import_so_search(prefix, query, tags, output_folder, count)
    else:
        print("Don't recognize that command.")
        return -1
    return 0


if __name__ == "__main__":
    sys.exit(main())
