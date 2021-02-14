Forking, Joining as Maintainer, Becoming the Maintainer
--------
Everyone is allowed to fork.
- It is right there in the GitLab Terms of Service
- You need to to do pull requests.
- It is allowed by MIT license by way of not saying you can't
- Sometimes dev say, "please fork because I quit", e.g. Dephell and many others
- If the project is abandoned that is the only way forward

You might be reluctant to fork because
- You don't want to create two rival projects
    - Maybe there will be drama with the original maintainer
    - You're just one person and would like the help of as many people if possible
- Maybe the usual maintainers will come back to write more code
- The license situation isn't to your liking
- No one invited you to
- The maintainer explicitly told everyone to f'k off

How To Apply for Maintainer at so_pip
------
Just do create a PR, get it thru the process and say you'd like to be maintainer.

Follow the "when in rome" principle and follow when you can, already established conventions, for example
keep the build script passing, the unit test coverage high, the code well linted.

If your main contribution is to break the build script and unit tests because you don't believe in them,
then really want you want is a fork...


How To Fork
------
For a PR, just do it.

For a hard fork, consider either picking a new name, or giving the existing name a suffix, for example, so_pip4 in case
I have died and can't upgrade to python 4. Lot of examples of this where the new maintainer just wants to keep
the app or lib moving with the ecosystem.

Another hypothetical, if you think this code is a mess and you have an idea to massively refactor, please, go head and
create a fork with a new name. For an example of this, see minibuild, pynt and navio.

Unsolved problems
---------
Let say you want to fix just one bug or add just one feature. Without maintainer rights and access to the pypi
keys, you'd have to fork and create a whole new app, with a new pypi entry, potentially a new name. If twenty
people did this, there would be twenty slightly different versions
