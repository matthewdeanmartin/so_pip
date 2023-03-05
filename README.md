so_pip
======
Everyone copies code from StackOverflow, but no one is formalizing it.

This will vendorize the source code of question or answer into a folder and
generate the accessory files to make it look like a python package.

The feature-set overlaps a bit with [cookie cutter, vendorizing libraries and
stackoverflow search cli's](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md).

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
pipenv install so_pip --pre --skip-lock

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
Consider getting a [key](https://stackapps.com/apps/oauth/register) and adding a [.so_pip.ini file](https://github.com/matthewdeanmartin/so_pip/blob/main/.so_pip.ini) The app will make best efforts if you don't.
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
* [Contributing *answers* to StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/contributing.md) AKA, fixing answers you found.
* [Attribution Compliance](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/comply_with_cc_sa.md)
* [Contributing to so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CONTRIBUTING.md)
* [Code of Conduct for so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CODE_OF_CONDUCT.md)
