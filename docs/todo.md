TODO
----

RELEASE 1.0 Goals
-----------------
- check in example with bash script for each command
- `pip install so_pip` works for each example.
- Dockerfile
- tox for fast tests on 3.8, 3.9
- version pinning
- BUG- setup.cfg mess
- BUG- not all licenses found?
- BUG- Authors don't distinguish role

RELEASE 2.0 Goals
-----------------
- Jupyter notebooks
- Content-only folders
- Merged Question+One Answer Pattern

Things I can't do yet
---------------------
High priority
- no code for handling overwriting previously generated code (clean, ask, merge)
- switch between code in /src/ code in /package_name/ and code in just main.py
- Pin versions, e.g. `so_pip vendorize --answer=31049648 --revision=2`
- Enable minimal units of code re-use, such as wrapping in "def" block
- Caching API calls between invocations for X minutes
- Generate README.md
    - Table of conents
    - recap authors (date, author, license, contrib type- e.g. question, comment, revision)
- IPython/Juputer notebook stuff
   - Generate code file as .ipynb file
   - Parse code that was copy/pasted to a code block.
     e.g. https://stackoverflow.com/questions/25748473/python-text-based-adventure-game-need-assistance
- Exploit shebangs (#!/usr/bin/python) to indicate code block should be a file
- Guess file name based on the line above the code block.
- Include comments in the questions/answers text or comments

Nice to have
- Get code from pastebin, gists or the like:
   - e.g. https://stackoverflow.com/questions/26188763/python-3-x-text-based-adventure-game-save-game-function
- Target a python version or detect which python versions are possible

Maybe will never figure out
------
- Can't replace constants with parameters (ie. example code works on constants, re-usuable code needs parameters)
- Handle ad-hoc templating, e.g. `print(<your name goes here>)`
- Give modules short semantic names
- Detect "pointless" constants (usually evaluated output from previous expression, i.e. not code but output.)
- Fix broken indents
- Detect when code is meant to be a "diff"
