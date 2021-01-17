so_pip
======
Everyone copies code from StackOverflow, but no one is formalizing it.

This will vendorize the source code of question or answer into a folder and
generate the accessory files to make it look like a python package.

The feature-set overlaps a bit with [cookie cutter, vendorizing libraries and
stackoverflow search cli's](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md).

Installation
------------
Requires Python 3.7+, tested with 3.7, 3.8, 3.9
```
pip install so_pip
so_pip vendorize my_name --question=31049648 --output=output
```


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
* [CLI](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/cli.md)
* [Code reuse scanarios you see on StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/scenarios.md)
* [Features](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/features.md)
* [Security Considerations](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/security.md)
* [Prior Art](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md) Similar and overlapping tools.
* [Contributing *answers* to StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/contributing.md) AKA, fixing answers you found.
* [Attribution Compliance](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/comply_with_cc_sa.md)
* [Contributing to so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CONTRIBUTING.md)
* [Code of Conduct for so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CODE_OF_CONDUCT.md)
