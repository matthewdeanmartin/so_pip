TODO
----

Things I can't do yet
---------------------
- no code for handling overwriting previously generated code
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
- Target a python version or detect which python versions are possible

Maybe will never figure out
------
- Can't replace constants with parameters (ie. example code works on constants, re-usuable code needs parameters)
- Handle ad-hoc templating, e.g. `print(<your name goes here>)`
- Give modules short semantic names
- Detect "pointless" constants (usually evaluated output from previous expression, i.e. not code but output.)
- Fix broken indents
- Detect when code is meant to be a "diff"
