Prior Art
---------

SO Browsers
-----------
- [howdoi](https://github.com/gleitz/howdoi) Search several sources including StackOverflow & screen scrape the source code.
- [socli](https://github.com/gautamkrishnar/socli) One of many command line interfaces to StackOverflow

so_pip differs from in the above in that the goal is to generate re-usable code, not just get you to the place where
you can copy-paste

Template Generators
-------------------
- [cookiecutter](https://github.com/cookiecutter/cookiecutter) Generate a python project shell with a variety of templates

Cookie cutter works off a static json file. Someday it might be worth having so_pip generate a json file to go with a
template optimized for an SO answer. Cookie cutter doesn't handle package workflows, such as updating (as far as I know)

PIP
---
Pip and related tools handle intentially created packages with source probably in GitHub and packages stored in pypi.

You could publish a so_pip created package to pypi, (possibly not a good idea), but so_pip packages are better vendorized.


Vendorization
-------------
- [vendorize](https://pypi.org/project/vendorize/)
- [vendy](https://pypi.org/project/vendy/)

so_pip's workflow makes the most sense when you are mostly taking over the source code of a "package" and putting it in
your own codebase

Virtual Environments
---------------------
- `pip install somepackage.tar.gz --target vendor` Installing from a local package to a local folder, then editing PYTHONPATH
- `python -m venv venv` Creating a venv virutal environment folder & checking it in, activate environment instead of editing PYTHONPATH
