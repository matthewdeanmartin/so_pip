Workflows
---------

One-and-Done
------------
Search stackoverflow and find a ready-to-go answer. More rarely, just the question has the code you want.

`so_pip vendorize --answer=123 --output=output`

All-in-One
----------
Search stackoverflow and find a question with many good, different answers, that all should be included.

`so_pip vendorize --question=123 --output=output --all-in-one`

Merge Question and One Answer
----------
Find an answer, except most of the code for the answer is in the question. Question and answer need to be manually merged.

Search with so_pip
----------
Let so pip do a search and generate all the answers that have re-usable code. Because this can be a lot
of crap, you will want to have quality filters set up, e.g. set minimum lines of code, etc.

`so_pip vendorize --question=123 --output=output --all-in-one`

Interactively Execute
---------------------
Find a question that has many, many code block interspersed with text. Convert these to notebooks and
execute them cell by cell to get better feel for what the concepts are. Not really a code re-use pattern.

Fork and Leave
-------------
Create a package in any of the above ways. Change code, never look back at StackOverflow.

Curate and Update
-------------
Create your own answer edit it on stackoverflow. Use revision feature to periodically
regenerate. If you have enough reputation, you can edit other people's answers.
