## Table of contents
* [General info](#general-info)
* [Setup](#setup)

## General info
This project is code extracted from the question ["Return a list of imported Python modules used in a script?"](https://stackoverflow.com/questions/2572582/return-a-list-of-imported-python-modules-used-in-a-script/2572654#2572654)

## Setup
To build and install this package:

```
# Read code to see if it all looks legit
$ python setup.py build bdist_wheel
# copy vendor_packages folder to your code base
# Add vendor folder to PYTHONPATH
$ pip install vendor_packages/*.whl -t vendor
```
Don't push to pypi unless you put substantial effort into it, pypi is already full of junk.

Credits and License
-------------------
Lasse V. Karlsen <https://stackoverflow.com/users/267>
Jono Bacon <https://stackoverflow.com/users/308456>
