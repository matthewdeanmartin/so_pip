Scenarios
---------
StackOverflow code normally executes on your brain. so_pip would like it to execute as a
re-usable package. Almost no one writes answers that way.

Functions and Classes
---------------------
This is where so_pip shines and copy-paste really can be a way of life.

Code already has some unit of re-used and sometimes even sample executions or tests.

For example:
```
def hypoteneuse(a, b):
    return sqrt(a**2 + b**2)

hypoteneuse(2, 3)
```
The sample execution will run on `import` so it needs to become

```
def hypoteneuse(a, b):
    return sqrt(a**2 + b**2)

if __name__ == "__main__":
    hypoteneuse(2, 3)
```

Scripts
-------
Code doesn't have a `def` or `class` and all code would execute immediately on import.

At minimum, you'd need to wrap it in a `def` block and convert constants to parameters

For example:
```
two = 1 + 1
print(two)
```
becomes
```
def print_sum(addor, addend):
    result = addor + addend
    print(result)
```

We can add some safety by adding a `def run()` header and footer, but not a lot of value.
```
def run():
    two = 1 + 1
    print(two)
if __name__ == "__main__":
    run()
```

Depressingly, at that point, so_pip is acting more like a solution skeleton generator
than a package generator.

One liners and inline code
--------------------------
These are just about unusable, sometimes it is just an abuse of markdown to highlight a word.

For example:
> You just need to `pip install requests` and then write a few lines of code.

> You just need to define a `def` than returns `sqrt(a**2 + b**2)`

> You should think of using `Jupyter`

```sqrt(a**2 + b**2)```

Yes there is code there, it is just about impossible to extract.


Interactive Sessions
--------------------
These are often a mix of interactive shell and interactive python REPL. They are good
candidates for turing into Jupyter notebooks.

For example:
```
$ python
>>>1 + 1
2
>>> print("two")
two
```

Almost Interactive Session
--------------------------
This is where you have a code block and the next block is actually the output.

For example:
```
def hypoteneuse(a, b):
    return "The answer is " + str(sqrt(a*2 + b*2))
```

```
The answer is 33
```

If people always wrote valid python, this would be no problem. The code would parse and the output would be identified
as "not python." In practice, output sometimes looks like valid but "useless" literals, sometimes real python
is so poorly indented or buggy it isn't recognizable as python.

Since I'd expect most people will need to edit code before using it, language detection should error on the side of
calling too many blocks python

The LANGUAGE_DETECTION section of the .so_pip.ini file helps tune this.

"Diffs"
--------
The original poster shows some broken code and the answer is a diff

```
def hypoteneuse(a, b):
    return sqrt(a*2 + b*2)
```
is answered with
```
    return sqrt(a**2 + b**2)
```

I think that doing a merge between these two blocks can't reliably be done and this is the simple scenario.
Sometimes, the diff code is even more complex or might have no similarity to the original code.

Just English
------------
These are noise-- either the question or the answer is just natural language text. At best, it can be
imported as comments in case the other parts of the post does have reusable code.

Not (All) Python
----------------
Python unavoidably is a mix of .py, .sh, .ini and other source code types. Django development is
even more complex with .js, .html, .css, etc.

These can be imported either by commenting out the non-python or, if language detection succeeds,
creating a file for each.

It is on my wish list to generate packages for other languages, but "to ship is to choose".

COMMENT_OUT_BAD_PYTHON and POSSIBLE_LANGUAGES help tune how we handle this.

Multiple Modules or One Module with comments?
---------------------------------------------
If an answer has six two line code blocks, it is probably one (abstractly speaking) file with commenting.

If an answer is two blocks, if each starts with a shebang or `import` it likely is a new file.

For example, this probably is meant to be two files
```
import requests
requests.get("https://google.com", timeout=10)
```

```
import pandas
data = pandas.read_csv("data.csv")
```

Some people use a convention of putting a file name right above the block

hello_world.py
```
print("hello world")
```
