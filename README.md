so_pip

What
----
Everyone copies code from StackOverflow, but no one is formalizing it.

This will vendorize the source code of question or answer into a folder and
generate the accessory files to make it look like a python package.

The feature set overlaps a bit with cookie cutter, vendorizing libraries and stackoverflow search cli's.

Docs
-----
* [Code reuse scanarios you see on StackOverflow](docs/scenarios.md)
* [Prior Art](docs/prior_art.md) Similar and overlapping tools.
* [Contributing *answers* to StackOverflow](docs/contributing.md) AKA, fixing answers you found.
* [Contributing to so_pip](CONTRIBUTING.md)
* [Code of Conduct for so_pip](CODE_OF_CONDUCT.md)

Usage for Beta
--------------
Consider getting a [key](https://stackapps.com/apps/oauth/register) and adding a [.so_pip.ini file](.so_pip.ini)

The app will make best efforts if you don't.
```
# Various way to get some code
> so_pip vendorize --question=31049648
> so_pip vendorize --answer=31049648
> so_pip search --answer=31049648
```

```
> so_pip uninstall {package_name}
> so_pip upgrade {package_name}
> so_pip list
> so_pip freeze
```

Security Considerations
-----------------------
Ha, ha, ha... ok, now seriously.

- Read code before you run it
- Do not run this as part of an automated build pipeline
- Only run this interactively
- This app won't run code from StackOverflow, you'll have to run that code.

[Copying code from stackover flow ...](https://stackoverflow.blog/2019/11/26/copying-code-from-stack-overflow-you-might-be-spreading-security-vulnerabilities/)
- Consider using this plugin: https://github.com/paper-materials-crowd-sourced/materials/tree/master/web-extension

[Scholars have studied code reuse from SO](https://link.springer.com/article/10.1007/s10664-018-9634-5)

Security Features
-----------------
- Runs safety on inferred package list
- Put everything into setup.cfg and almost noting in setup.py.
- TODO: Optionally wrap all code in def run(): and if name=main: run()
- TODO: Support pinning to a known version


Things I can do now
-------------------
With help from a lot of libraries
- Extract python blocks from HTML
    - Generally assume that code is non-python comments interspersed with one files worth of code.
    - Add module header with authorship and license info
    - Add Question code when answers make sense only with question, e.g. https://stackoverflow.com/questions/65373654/cant-figure-out-how-to-check-my-list-and-input-with-each-other
    - Handle questions with no answers.
- Guess principle language and provide suitable extension (Partially implemented)
    - Check if valid python expression (not very strict)
        - optionally comment out bad python
- Clean up python
    - Handle interactive console syntax (e.g. >>> and ... prefixes)
    - Upgrade python to 3.x
    - Format it with black and isort
- Generate supporting files
    - Include html file for diagnostics
    - Format HTML as text without losing too much markup
    - Generate requirements.txt (sometimes)
    - Add LICENSE file based on each revision's license
        - Handle multiple licenses
    - Add AUTHORS file based on revisions
        - Parsable authors with links
    - Add CHANGELOG
        - Changelog supports two schemas (almost)
    - Add Code of Conduct
- Splits source code across files when the are clues it should be many files
- Turn code file(s) into python package
    - Generate version from answer revision
    - package dependencies for requirements.txt and setup.py
        - find imports from source
        - remove system modules
        - check if package exists, assuming package name is module name
        - pins requirements to latest versions on pypi
        - runs `safety` to see if inferred packages are safe
- CLI
    - Primative versions of Freeze, List, Show
    - `vendorize` to distinguish from real `pip install`

