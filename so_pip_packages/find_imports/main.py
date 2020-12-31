"""
Author: Daniel G
Author Link: https://stackoverflow.com/users/207432/daniel-g
License: CC BY-SA 2.5
Date: 2010-04-03 16:57:45
Answer Url: http://stackoverflow.com/questions/2572582/2572654#2572654
"""

import imp
# Well, you could always write a simple script that searches the file for
# `import` statements. This one finds all imported modules and files, including
# those imported in functions or classes:
from typing import List


def find_imports(toCheck: str, importable_only: bool = False) -> List[str]:
    """
    Given a filename, returns a list of modules imported by the program.
    Only modules that can be imported from the current directory
    will be included. This program does not run the code, so import statements
    in if/else or try/except blocks will always be included.
    """
    importedItems = []
    with open(toCheck, encoding="utf-8", errors="ignore") as pyFile:
        for raw_line in pyFile:
            # ignore comments
            line = raw_line.strip().partition("#")[0].partition(" as ")[0].split(" ")
            if line[0] == "import" or line[0]=="from":
                process_line(importable_only, importedItems, line)

    return importedItems


def process_line(importable_only, importedItems, line):
    for imported in line[1:]:
        if imported == "import":
            break

        # remove commas (this doesn't check for commas if
        # they're supposed to be there!
        imported = imported.strip(", ")
        try:
            # check to see if the module can be imported
            # (doesn't actually import - just finds it if it exists)
            imp.find_module(imported)
            # add to the list of items we imported
            importedItems.append(imported)
        except ImportError:
            # ignore items that can't be imported
            # (unless that isn't what you want?)
            if not importable_only:
                importedItems.append(imported)


if __name__ == "__main__":
    # toCheck = eval(input("Which file should be checked: "))
    print(find_imports("question_1_.py"))

# This doesn't do anything for `from module import something` style imports,
# though that could easily be added, depending on how you want to deal with
# those. It also doesn't do any syntax checking, so if you have some funny
# business like `import sys gtk, os` it will think you've imported all three
# modules even though the line is an error. It also doesn't deal with
# `try`/`except` type statements with regards to import - if it could be
# imported, this function will list it. It also doesn't deal well with multiple
# imports per line if you use the `as` keyword. The real issue here is that I'd
# have to write a full parser to really do this correctly. The given code works
# in many cases, as long as you understand there are definite corner cases.
#
# One issue is that relative imports will fail if this script isn't in the same
# directory as the given file. You may want to add the directory of the given
# script to `sys.path`.
