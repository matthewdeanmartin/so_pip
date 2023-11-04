so_pip
======
Everyone copies code from StackOverflow, but no one is formalizing it.

`so_pip` will vendorize the source code of question or answer into a folder and
generate the files to make into a python package.

`so_pip` is less like a package installer and more like a project template maker, [cookie cutter, vendorizing libraries
and stackoverflow search cli's](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md).

## so_pip is dead, the AI version might actually be useful

Ever think, "I wish I could pip install the answer to this stackoverflow question?"
You almost could with some markdown parsing and vendorizing techniques.

But too many answers were not given in the form of a function or a class, so they lack
the minimal conditions for code re-use. There is no non-AI way to turn a script into
a re-usable function, so this approach was always fatally flawed.

See the soon-to-be-posted "ai_pip" project that will do the same thing but use ChatGPT
to transform the answer into re-usable code. This will solve previously unsolvable problems,
like:

- What code is this? Is that python or bash?
- Is this series of markdown blocks one code file per block?
- Is this series of markdown code blocks actually one code file with comments?
- What is a good name for the package?
- Is the code in the question part of the code in the answer?
- If this code was written to be re-usable, what would it look like?
- How do we upgrade the code to modern python?
- Is the code malicious or buggy?
- Where are the tests?

Badges
------

![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/so-pip)
[![Downloads](https://pepy.tech/badge/so-pip/month)](https://pepy.tech/project/so-pip/month)
[![CodeFactor](https://www.codefactor.io/repository/github/matthewdeanmartin/so_pip/badge)](https://www.codefactor.io/repository/github/matthewdeanmartin/so_pip)

Installation
------------
Requires Python 3.11+

```
pip install so_pip
# or
poetry install so_pip

so_pip vendorize my_name --question=31049648 --output=output
```

Using via [dockerhub](https://hub.docker.com/repository/docker/matthewdeanmartin/so_pip)

```
# for mac, unix, cmd.exe, powershell
docker pull matthewdeanmartin/so_pip
docker run --rm -i -v "$PWD/data:/data" matthewdeanmartin/so_pip --help
```

If you use git bash/mingw64/cygwin, see [run.sh](https://github.com/matthewdeanmartin/so_pip/blob/main/docker/run.sh)
because docker needs help doing a volume mount.


Usage
--------------
Consider getting a [key](https://stackapps.com/apps/oauth/register) and adding
a [.so_pip.ini file](https://github.com/matthewdeanmartin/so_pip/blob/main/.so_pip.ini) The app will make best efforts
if you don't.

```
# Turn posts into nicely formated packages
> so_pip vendorize my_name --question=31049648 | --answer=31049648
> so_pip search --answer=31049648 --tags=python

# Pip-like commands
> so_pip uninstall | upgrade {package_name}
> so_pip list | freeze
```

Docs
-----

* [Examples](https://github.com/matthewdeanmartin/so_pip/tree/main/examples)
* [Workflows](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/workflows.md)
* [CLI](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/cli.md)
* [Code reuse scanarios you see on StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/scenarios.md)
* [Features](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/features.md)
* [Security Considerations](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/security.md)
* [Prior Art](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md) Similar and overlapping tools.
* [Contributing *answers* to StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/contributing.md)
  AKA, fixing answers you found.
* [Attribution Compliance](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/comply_with_cc_sa.md)
* [Contributing to so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CONTRIBUTING.md)
* [Code of Conduct for so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CODE_OF_CONDUCT.md)
