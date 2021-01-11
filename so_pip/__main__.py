# noinspection PyPep8
"""so_pip/StackOverflow Pip
Not associated with PyPA, nor StackOverflow.

Usage:
  so_pip vendorize <name> (--question=<question_id>|--answer=<answer_id>|--package=<package>) [--revision=<revision>] [options]
  so_pip search <name> --query=<query> --tags=<tags> [--count=<count>] [options]
  so_pip uninstall <names>... [options]
  so_pip list [options]
  so_pip freeze [options]
  so_pip show <names>... [options]
  so_pip (-h | --help)
  so_pip --version

Options:
  -h --help                    Show this screen.
  -v --version                 Show version.
  -c --count=<count>           How many posts to get [default: 2].
  -o --output=<output>         Folder for packages. Defaults to /output
  -q --question=<question_id>  Stackoverflow question id
  -a --answer=<answer_id>      Stackoverflow answer id
  -r --revision=<revision>     Revision id for answer.
  --verbose                    Show logging
  --quiet                      No informational logging

"""
import logging
import sys

import docopt

from so_pip import _version as meta
from so_pip import settings as settings
from so_pip.commands import freeze as freeze
from so_pip.commands import list_all as list_all
from so_pip.commands import search as search
from so_pip.commands import show as show
from so_pip.commands import uninstall as uninstall
from so_pip.commands import vendorize as vendorize

# Do these need to stick around?
LOGGERS = []

LOGGER = logging.getLogger(__name__)


def main() -> int:
    """Get the args object from command parameters"""
    arguments = docopt.docopt(__doc__, version=f"so_pip {meta.__version__}")
    # print(arguments)
    # LOGGER.debug(arguments)
    output_folder = arguments["--output"]
    if arguments["--quiet"]:
        settings.QUIET = True

    if arguments["--verbose"]:
        # root logger, all modules
        for root in ("so_pip", "__main__", "url_lib3"):
            logger = logging.getLogger(root)
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            LOGGERS.append(logger)
    if arguments["vendorize"]:
        prefix = arguments["<name>"] or ""
        question = arguments["--question"]
        answer = arguments["--answer"]
        revision = arguments["<revision>"]
        if not question and not answer:
            print("Must specify --question or --answer identifier")
            return -1
        if not output_folder:
            print("No --output folder specified")
            return -1
        if question:
            packages_made = vendorize.import_so_question(
                prefix, question, output_folder
            )
        elif answer:
            packages_made = vendorize.import_so_answer(
                prefix, answer, output_folder, revision
            )
        else:
            raise TypeError("Need to specify a question or answer")
        print(f"Vendorized {','.join(packages_made)} at {output_folder}")
    elif arguments["uninstall"]:
        packages = arguments["<name>"]
        if not packages:
            print("No packages specified to uninstall")
            return -1
        for package in packages:
            uninstall.uninstall_package(output_folder, package)
        print(
            f"Uninstalled {','.join(packages)} from vendorized folder.\n"
            f"If you also installed with pip you will need to uninstall with pip"
        )
    elif arguments["list"]:
        if not output_folder:
            print("Missing --output folder")
            return -1
        list_all.list_packages(output_folder)
    elif arguments["freeze"]:
        if not output_folder:
            print("Missing --output folder")
            return -1
        freeze.freeze_environment(output_folder)
    elif arguments["show"]:
        packages = arguments["<names>"]
        if not packages:
            print("No packages specified to show")
            return -1
        for package in packages:
            show.show(output_folder, package)
    elif arguments["search"]:
        prefix = arguments["<name>"]
        if not prefix:
            prefix = ""
        query = arguments["--query"]
        if not query:
            print("--query required for search")
            return -1

        try:
            count_str = arguments["--count"]
            count = int(count_str)
        except ValueError:
            print(f"Can't convert {arguments.get('--count', '')} to a number")
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
