"""
CC BY-SA 3.0 Jeffeb3
http://stackoverflow.com/questions/2572582/25690011#25690011
"""

# I was looking for something similar and I found a gem in a package called
# [PyScons](https://pypi.python.org/pypi/PyScons). The Scanner does just what
# you want (in 7 lines), using an import_hook. Here is an abbreviated example:
import modulefinder
import sys


class SingleFileModuleFinder(modulefinder.ModuleFinder):
    def import_hook(self, name, caller, *arg, **kwarg):
        if caller.__file__ == self.name:
            # Only call the parent at the top level.
            return modulefinder.ModuleFinder.import_hook(
                self, name, caller, *arg, **kwarg
            )

    def __call__(self, node):

        self.name = str(node)

        self.run_script(self.name)


if __name__ == "__main__":
    # Example entry, run with './script.py filename'
    print("looking for includes in %s" % sys.argv[1])

    mf = SingleFileModuleFinder()
    mf(sys.argv[1])

    print("\n".join(list(mf.modules.keys())))
