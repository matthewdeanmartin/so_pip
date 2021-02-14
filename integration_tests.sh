set -euxo pipefail
#Usage:
#  so_pip vendorize <name> (--question=<question_id>|--answer=<answer_id>|--package=<package>) [--revision=<revision>] [options]
#  so_pip search <name> --query=<query> --tags=<tags> [--count=<count>] [options]
#  so_pip uninstall <names>... [options]
#  so_pip list [options]
#  so_pip freeze [options]
#  so_pip show <names>... [options]
#  so_pip (-h | --help)
#  so_pip --version
#
#Options:
#  -h --help                    Show this screen.
#  -v --version                 Show version.
#  -c --count=<count>           How many posts to get [default: 2].
#  -o --output=<output>         Folder for packages. Defaults to /output
#  -q --question=<question_id>  Stackoverflow question id
#  -a --answer=<answer_id>      Stackoverflow answer id
#  -r --revision=<revision>     Revision id for answer.
#  --all-in-one                 Combine all code into one module
#  --verbose                    Show logging
#  --quiet                      No informational logging
python -m so_pip --help
python -m so_pip --version
python -m so_pip list --output=output
python -m so_pip freeze --output=output
# not implemented?
# python -m so_pip --show foobar --output=output

python -m so_pip vendorize int_test1 --question=29312494 --verbose --output=output
python -m so_pip vendorize int_test2 --answer=3768975 --revision=1 --verbose --output=output
python -m so_pip vendorize int_test2 --answer=12927726 --verbose --output=output
python -m so_pip vendorize int_test3 --package=lua_a_healthy_earlier --revision=1 --verbose --output=output
python -m so_pip vendorize int_test4 --question=29312494 --all-in-one --verbose --output=output
python -m so_pip vendorize int_test1 --question=29312494 --quiet --output=output
python -m so_pip search rust --query="send email" --tags=rust --count=2 --output=output
