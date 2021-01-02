"""
CC BY-SA 3.0 Tony Suffolk 66
http://stackoverflow.com/questions/2572582/22441743#22441743
"""

import importlib as implib

# This works - using importlib to actually import the module, and inspect to get
# the members :
#! /usr/bin/env python
#
# test.py
#
# Find Modules
#
import inspect

if __name__ == "__main__":
    mod = implib.import_module("example")
    for i in inspect.getmembers(mod, inspect.ismodule):
        print(i[0])

#! /usr/bin/env python
#
# example.py
#
import sys
from os import path

if __name__ == "__main__":
    print("Hello World !!!!")

#
# Output :
# tony@laptop .../~:$ ./test.py
# path
# sys
