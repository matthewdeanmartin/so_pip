Command Line Interface
----------------------
```
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
  --verbose                       Show logging
  --quiet                      No informational logging

```
so_pip vendorize
----------------
Generates one or more package based on a question or answer.

If you provide a revision number, only one package will be generated.

so_pip search
-------------
Generate packages for all questions and answers returned by query. Stops after 2 questions.

so_pip uninstall/list/freeze/show
--------------------------------
Deletes and lists folders lists. Show displays metadata for a package.

Options
-------
--output Defaults to /output/
