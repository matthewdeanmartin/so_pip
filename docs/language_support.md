Programming languages supported
-------------------------------
I'm using the `whats_that_code` library to identify a programming language in a snippet.


Default
-------
If I don't know much about the programming language you get gnits style project documentation files
and a coding file with hopefully the correct extension.

Python
------
`so_pip` is implemented in python so it has the most python specific features.

Language specific features
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
npm package support is on the roadmap.

Lua
-------
lua rocks package support is on the roadmap.

C#/nuget
-------
C# nuget package support is on the roadmap.