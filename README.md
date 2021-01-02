so_pip
======
Everyone copies code from StackOverflow, but no one is formalizing it.

This will vendorize the source code of question or answer into a folder and
generate the accessory files to make it look like a python package.

The feature-set overlaps a bit with [cookie cutter, vendorizing libraries and
stackoverflow search cli's](docs/prior_art.md).

Installation
------------
```
git clone https://github.com/matthewdeanmartin/so_pip.git
pip install -e .
# some tools can't co-exist in the same virtual environment
pipx install pylint
pipx install isort
```
I'll publish to pypi and make a Dockerfile soonish.

Usage
--------------
Consider getting a [key](https://stackapps.com/apps/oauth/register) and adding a [.so_pip.ini file](.so_pip.ini) The app will make best efforts if you don't.
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
* [Examples](examples)
* [CLI](docs/cli.md)
* [Code reuse scanarios you see on StackOverflow](docs/scenarios.md)
* [Features](docs/features.md)
* [Security Considerations](docs/security.md)
* [Prior Art](docs/prior_art.md) Similar and overlapping tools.
* [Contributing *answers* to StackOverflow](docs/contributing.md) AKA, fixing answers you found.
* [Attribution Compliance](docs/comply_with_cc_sa.md)
* [Contributing to so_pip](CONTRIBUTING.md)
* [Code of Conduct for so_pip](CODE_OF_CONDUCT.md)
