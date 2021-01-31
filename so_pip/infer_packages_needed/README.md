This will infer what packages are needed given python source code.

Common techniques to get basic list of dependencies
- string parsing of the python.
- ast/astroid parsing of python
- using dis, inspect, imp, importlib to do more than just parse, maybe actually run the import
- import and inspect what is in scope

The above does not get you the pypi package name!

Things needed to get package name:
- list of all packages.
- top level modules for all packages
    - requires downloading all packages on pypi (6TB for all!)
    - this makes most sense for maybe top N packages
    - or packages with fewer downloads but some other metric
