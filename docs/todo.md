TODO
----

RELEASE 1.0 Goals
-----------------
- Feature: Infer minimum python version & fill in pyproject.toml & Readme.md.
- Feature: Change most support files to .md
- BUG: setup.cfg is a mess.
- BUG: not all licenses found?
- BUG: Pyproject.toml
    - classifiers don't take into account min/max python version
- UX:
    - just 1 question
    - pinned question
    - version pinning, 1/2 done, answers-only by revision
- Test needed: code files other than python poorly tested.
- Test needed: check in example with bash script for each command, 1/2 done
- Test needed: `pip install so_pip` works for each example, but only for sdist
    - integration test & run sdist package for each.
- Dockerfile, 1/2 done
    - mount volume
- Performance: Caching API calls between invocations for X minutes
    - Investigating disk caching. @lru caching already in place, but limited value.
- FEATURE: update_any module
    - no code for handling overwriting previously generated code (clean, ask, merge)
- Carve out "subprojects"
    - guess_language
    - bad_words
    - random_names
    - pypi_query


RELEASE 2.0 Goals
-----------------
- UX: colored console flash, emojis, animations
- IPython/Jupyter notebook stuff
   - Generate code file as .ipynb file
   - Parse code that was copy/pasted to a code block.
     e.g. https://stackoverflow.com/questions/25748473/python-text-based-adventure-game-need-assistance
- Content-only folders for codeless q & a.
    - Mostly so that when code is missing from post, so_pip code that expects code doesn't run.
- Merged Question+One Answer Pattern
    - Basically, install question.py and answer.py instead of main.py
- switch between code in /src/ code in /package_name/ and code in just main.py
    - /package_name/src/package_name pattern for python only.
- Pin versions, e.g. `so_pip vendorize --answer=31049648 --revision=2`
    - 1/2 done, but a single question should be pinnable, but questions grab all answers!
- Enable minimal units of code re-use, such as wrapping in "def" block
    - 1/2 done, need to wire up to `settings`
- Generate README.md
    - Table of contents with something sensible
    - recap authors (date, author, license, contrib type- e.g. question, comment, revision)
- Extract file name based on the line above the code block (regex find any file name candidates?)
- Include comments in the questions/answers text or comments

Release 3.0
-----------
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
