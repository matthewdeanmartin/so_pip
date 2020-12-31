so_pip

What
----
Everyone copies code from StackOverflow, but no one is formalizing it.

This will vendorize the source code of question or answer into a folder and
generate the accessory files to make it look like a python package.

Usage for Alpha
---------------
Pipenv install, edit settings.py, script/try_out.py & run. Look at
results in output folder. Vendorize module or `pip -e` install it.

Usage for Beta
--------------
PARTIALLY IMPLEMENTED
```
# question and all it's answers
> so_pip vendorize --question=31049648
See output/ for results.
Vendorized {package_name}, {package_name}, ... to so_pip_packages/

# Just the one good answer
> so_pip vendorize --answer=31049648
Vendorized {package_name} to so_pip_packages/

> so_pip uninstall {package_name}
Removed {package_name} from so_pip_packages/

> so_pip upgrade {package_name}
Removed {package_name} from so_pip_packages/

> so_pip list
{package_name}
{package_name}

> so_pip freeze
{package_name}
{package_name}
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

Things I can't do yet
---------------------
- Pin versions, e.g. `so_pip vendorize --answer=31049648 --revision=2`
- Get code from pastebin, gists or the like:
   - e.g. https://stackoverflow.com/questions/26188763/python-3-x-text-based-adventure-game-save-game-function
- Generate README.md
    - Table of conents
    - recap authors (date, author, license, contrib type- e.g. question, comment, revision)
- IPython/Juputer notebook stuff
   - Generate code file as .ipynb file
   - Parse code that was copy/pasted to a code block.
     e.g. https://stackoverflow.com/questions/25748473/python-text-based-adventure-game-need-assistance
- Code comment syntax is python even though I can figure out that the main chunk of code is not python
    - root problem is how to detect programming language when it isn't perfect python
- Enable minimal units of code re-use, such as wrapping in "def" block
- Caching
- Exploit shebangs (#!/usr/bin/python) to indicate code block should be a file
- Guess file name based on the line above the code block.
- Include comments in the questions/answers text or comments

Maybe will never figure out
------
- Can't replace constants with parameters (ie. example code works on constants, re-usuable code needs parameters)
- Handle ad-hoc templating, e.g. `print(<your name goes here>)`
- Give modules short semantic names
- Detect "pointless" constants (usually evaluated output from previous expression, i.e. not code but output.)
- Fix broken indents
- Detect when code is meant to be a "diff"
