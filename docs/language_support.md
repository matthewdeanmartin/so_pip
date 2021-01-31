Programming languages supported
-------------------------------
I'm using the `whats_that_code` library to identify a programming language in a snippet.


Default
-------
If I don't know much about the programming language you get gnits style project documentation files
and a coding file with hopefully the correct extension.

Generically, you can opt to put the code files into an SRC file or leave them in the package root.

Python
------
`so_pip` is implemented in python so it has the most python specific features.

Language specific features
- Supports extra folder for the module to hold the init file.
- formatting- calls out to `black`
- upgrading- calls out to `pyupgrade`
- generating dependency file by string parsing of source
- execute/import live code (probably only safe in a container)
    - e.g. run embedded unit tests
    - detect dependencies
- parse the AST (without )
    - detect re-usable code


XML, yaml, json
---------------
Not really programming languages, but when found, I can parse these and get a strong signal
that I have valid "code".

JavaScript
-------
- can detect js
- Generates basic package.json file
- TODO: usage instructions for use as local, non-npm package
- Can't yet detect what version of js/node code is

Lua
-------
- can detect lua
- Generates basic rockspec file
- Can parse generated rockspec to see if it a valid lua table
- Can't detect minimum lua version
- Looks like it could be easy to get 1st pass on dependencies from "requires" statements

C#/nuget
-------
- can detect cs
C# nuget package support is on the roadmap.

Go
---
- can detect go
- TODO: Looks like it would be easy...

Ruby
-------
- can detect ruby
- Generates basic gemspec file
