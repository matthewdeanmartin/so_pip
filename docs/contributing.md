Contributing Answers
--------------------
This is about how to contribute to an answer you found in StackOverflow to make the code more re-usable.

You need 2000 reputation points to edit & even more to edit without peer review.

See CONTRIBUTING.md for how to contribute to so_pip the tool.

First: Do no harm
-----------------
I wrote this tool as a joke. Don't go turn someones beautiful 10 line answer into a 3000 line monster just to
make it more importable.

I think it is always safe to
- fix indentation and syntax errors
- change blockquote to code block if it is source code
- add language hint, e.g. lang-py
- add a [python] tag if there are enough space to add another tag
- add `imports` (if it is just a few)
- clean up people's Markdown and English.
- upgrade 2.x only code to 2.7/3.x code, for example, `print "yo"` to `print("yo")`

I think it is a grey area to
- change scripts to re-usable code, i.e. `def`s and `class`es
- upgrade a 2.x answer to 3.x only code
- correct the syntax of a question. The answers might become incoherent if the question is perfect code.
- renaming all the variables to follow modern conventions

Use judgement when you are in the grey area.

I think it isn't a good idea to
- Change answer style from IPython/Jupyter style to a single code block.
- Turn one-liners into 100 liners, turn 100 liners into 1000 liners.
- Add features unrelated to the question
- Handle too many scenarios if the question wasn't about covering all scenarios

Use judgement if you think you have an exception to the guideline.

Comparison to Github
--------------------
- Edits not Pull Requests.
- Edits are approved automatically, but can be reverted.
- Editing requires enough reputation for the site to consider you trust worthy.
- New answers instead of Forks. SO has no concept of a "forked answer"
- StackOverflows code of conduct governs, cf GitHub where each project has a different code of conduct

Post a new answer if a major rewrite is needed
----------------------------------------------
"Diff" answers (that show the corrected version of one line of code from a 100 line code block the original poster wrote)
are awful for so_pip. But they are easy on the eyes for humans to read.

To correct a "Diff" answer and make it consumable by so_pip, post a new answer. There still might be drama with
people complaining if the answer doesn't "add" something new that hasn't already been said.

Perfect Answer
------------------
``` lang-py
def hypoteneuse(a, b):
    return sqrt(a*2 + b*2)
if __name__ =="__main__":
    assert hypoteneuse(4,5)>=4 and hypoteneuse(4,5)>=5
```
* Answer with a function with parameters instead of script.
* Exercise code with `if __name__ =="__main__"` block
* Use built in testing structures like `assert` or `unittest`
* Specify the language of the code block
* include `imports` if any
* declare and initialize any variables

Python 2.x vs 3.x support
-------------------------
Sometimes the OP, ten years ago, asked for a 2.x answer. That guy might not even be alive now, so today
the audience is people who probably use 2.7 and 3.x. The least-drama solution is probably to update answers
to be 2.7/3.x compatible, or post a new answer that is 3.x compatible.
