so_pip

What
----
Everyone copies code from stack overflow, but no one is formalizing it.

Security Considerations
-----------------------
Ha, ha, ha... ok, now seriously.

- Read code before you run it
- Do not run this as part of an automated build pipeline
- Only run this interactively
- This app won't run code from StackOverflow, you'll have to run that code.
- (soon) I'll implement running `safety` on the inferred imported packages

[Copying code from stackover flow ...](https://stackoverflow.blog/2019/11/26/copying-code-from-stack-overflow-you-might-be-spreading-security-vulnerabilities/)
- Consider using this plugin: https://github.com/paper-materials-crowd-sourced/materials/tree/master/web-extension

[Scholars have studied code reuse from SO](https://link.springer.com/article/10.1007/s10664-018-9634-5)

Things I can do now
-------------------
With help from a lot of libraries
- Add module header with authorship and license info
- Extract python blocks from HTML
- Check if valid python expression (not very strict)
- Upgrade python to 3.x
- Format it with black and isort
- Guess principle language and provide suitable extension
- Include html file for diagnostics
- Format HTML as text without losing too much markup
- Generate requirements.txt (sometimes)
- Handle interactive console syntax (e.g. >>> and ... prefixes)
- Handle questions with no answers.
- Generally assume that code is non-python comments interspersed with one files worth of code. (violated when it
represents 2+ files)

Things I can't do yet
---------------------
- Add Question code when answers make sense only with question, e.g. https://stackoverflow.com/questions/65373654/cant-figure-out-how-to-check-my-list-and-input-with-each-other
- Can't cope with IPython/Juputer notebook stuff
- I can't tell a single line/single word of code from code tag being used on English for styling.
- Can't fix imports without making a mess
- Can't tell when some code blocks are "formulae" or "shell script" and rest is Python
- Code comment syntax is python even though I can figure out that the main chunk of code is not python
- Can't wrap in "def" block
- Can't replace constants with parameters (ie. example code works on constants, re-usuable code needs parameters)
- Give modules semantic names
- Detect "pointless" constants (usually evaluated output from previous expression, i.e. not code but output.)
- Fix broken indents
- Exploit shebangs (#!/usr/bin/python) to indicate code block should be a file
- Handle ad-hoc templating, e.g. `print(<your name goes here>)`
- submodule version from answer revision
- caching
