so_pip

What
----
Everyone copies code from StackOverflow, but no one is formalizing it.

This will vendorize the source code of question or answer into a folder and
generate the accessory files to make it look like a python package.

The feature set overlaps a bit with [cookie cutter, vendorizing libraries and
stackoverflow search cli's](docs/prior_art.md).

Docs
-----
* [Code reuse scanarios you see on StackOverflow](docs/scenarios.md)
* [Features](docs/features.md)
* [Security Considerations](docs/security.md)
* [Prior Art](docs/prior_art.md) Similar and overlapping tools.
* [Contributing *answers* to StackOverflow](docs/contributing.md) AKA, fixing answers you found.
* [Attribution Compliance](docs/comply_with_cc_sa.md)
* [Contributing to so_pip](CONTRIBUTING.md)
* [Code of Conduct for so_pip](CODE_OF_CONDUCT.md)

Usage for Beta
--------------
Consider getting a [key](https://stackapps.com/apps/oauth/register) and adding a [.so_pip.ini file](.so_pip.ini)

The app will make best efforts if you don't.
```
# Various way to get some code
> so_pip vendorize my_name --question=31049648
> so_pip vendorize my_name --answer=31049648
> so_pip search --answer=31049648 --tags=python
```

```
# Various workflow tasks
> so_pip uninstall {package_name}
> so_pip upgrade {package_name}
> so_pip list
> so_pip freeze
```
