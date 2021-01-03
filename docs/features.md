

Things I can do now
-------------------
- Convert question or answer HTML into one or more .py files
    - Header with authorship and license info
    - Comment out all non-code, optionally comment out code that doesn't parse.
    - File splits on blocks starting with `import`
- Guess principle language
    - Tag based guess
    - Markdown annotation based, eg. lang-py
    - Confirm as python by parsing (could still be bad python)
- Clean up python
    - Handle interactive console syntax (e.g. >>> and ... prefixes)
    - Upgrade python to 3.x
    - Deindent, format it with black and isort
- Generate supporting files to create [Gnu style](https://www.gnu.org/prep/standards/standards.html#Documentation)
 package/project folder
    - Write post out as html, txt and MD
    - Infer dependencies
        - Generate requirements.txt and dependencies section of setup.cfg
        - find imports from source
        - remove system modules
        - check if package exists, assuming package name is module name
        - pins requirements to latest versions on pypi
        - runs `safety` to see if inferred packages are safe
    - Add one or more license files to /LICENSE/ folder
    - Add AUTHORS.txt file based on revisions
        - Parsable authors with links
    - Add CHANGELOG.txt base on revisions
    - Add CODE_OF_CONDUCT.txt based on StackOverflows offical one
    - Generate version from answer revision
- CLI
    - Primative versions of Freeze, List, Show
    - `vendorize` to distinguish from real `pip install`