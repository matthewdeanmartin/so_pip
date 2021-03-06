TODO
----

RELEASE 1.0 Goals
-----------------
- BUG:
    - generic code files are missing brief header
    - more templates for code files? e.g. go/js/etc
- meta.so_pip file
    - has all the data for doing a subsequent update
- FEATURE: Better "re-usable code" detections
    - High lines of code
    - def/class syntax
    - has `__name__ == '__main__'` or assert or unittest
- FEATURE: specify entire module name for 1-offs
    - if only 1 module
    - e.g. so_pip vendorize --question 1234 --single_name=send_email ...
- FEATURE: Question as "all-in-one", put all code files into one python package
    - why? because some questions are like a library of all the ways to do a thing, e.g. zip a folder
    - now 1/2 done, needs better naming other than main1.py, etc.
- FEATURE: Merged Question+One Answer Pattern
    - Basically, install question.py and answer.py instead of main.py
- FEATURE: update_any module
    - no code for handling overwriting previously generated code (clean, ask, merge)
    - counter point- maybe 1% of answers are in a fully re-usable form
- Test needed: exercise workflow, check in example with bash script for each command, 1/2 done
- Run tool as Dockerfile, 1/2 done
    - mount volume
- UX: (see [workflows](workflows.md))
    - just 1 question
    - pinned question
    - version pinning, 1/2 done, answers-only by revision
- FEATURE: handle recogonizable datafiles
    - just json/xml/yaml - turn text into comments
    - json/xml/yaml, but for code to work, it needs to be a standalone file

*Supporting Files*
- BUG: not all licenses found?
- BUG: README talks about pypi for non-python code.
- TODO: support a few other languages
    - php, cs, lua, ruby, js/npm - 1/2 done
    - Fix attributes for various package specs
    - Needs "principal author"
- IPython/Jupyter notebook stuff
   - Generate code file as .ipynb file
   - Parse code that was copy/pasted to a code block.
     e.g. https://stackoverflow.com/questions/25748473/python-text-based-adventure-game-need-assistance

*Python version*
- Feature: Infer minimum python version & fill in pyproject.toml & Readme.md.
    - 1/2 done
- BUG: Pyproject.toml
    - classifiers don't take into account min/max python version

*Post packaging*
- Test needed: `pip install so_pip` works for each example, but only for sdist
    - integration test & run sdist package for each.

*Code debt, Reorg, Refactoring, Build Scripts*
- Carve out "subprojects"
    - guess_language - DONE
    - random_names - DONE
        - bad_words - Done but bundled with random names.
    - infer_packages_needed -
        - already solved 10 ways
        - but no one has solved "this module is in what pypi package(s)?"
        - maybe use datasette
- Code Debt: PackageObject should be more like a post object with optional language specific things
- TODO: Build with Makefile (in addition to regular build script)
- Performance: Switch(es) to turn off black/pylint/safety/etc

RELEASE 1.1
------------
- Feature: Add shebang if no reusable code (assume script)
- BUG: shebang gets stuck in middle
    - import_so_answer("unzip", 1855118, OUTPUT_FOLDER, revision_id=-1)

RELEASE 2.0 Goals
-----------------
- FEATURE: file name detection
- Make file (other build scripts?)
- FEATURE: SUPER MEGA SEARCH
    - multiquestion, multianswer search that
    - searches e.g. `[python] (def or class) is:answer email`
    - stricter defaults (skip content with no def/class, too little code)
    - questions as all-in-one
    - (general idea to avoid an explosion of folders & files)
    - turn off all slow bits (upgrading to py3, etc)
- UX: colored console flash, emojis, animations
- Content-only folders for codeless q & a.
    - Mostly so that when code is missing from post, so_pip code that expects code doesn't run.
- switch between code in /src/ code in /package_name/ and code in just main.py
    - /package_name/src/package_name pattern for python only.
    - counterpoint, putting 1 main.py file into a name module with dunder init is already overkill
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
- Run in two passes, first to gather up API calls, call in batch, re-run and get from cache.

Maybe will never figure out
------
- Can't replace constants with parameters (ie. example code works on constants, re-usuable code needs parameters)
- Handle ad-hoc templating, e.g. `print(<your name goes here>)`
- Give modules short semantic names
- Detect "pointless" constants (usually evaluated output from previous expression, i.e. not code but output.)
- Fix broken indents
- Detect when code is meant to be a "diff"
