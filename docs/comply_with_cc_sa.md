Compliance
-----------
There are plenty of lawyerly statements on the web that say CC BY SA licenses are incompatible with all common
software licenses and that there is no legal path to combining your code with CC BY SA code.

Yet everyone copy-pastes code from StackOverflow to their own code with no apparent harm & StackOverflow itself
encourages doing so as long as you make reasonable efforts to comply with the Attribution requirements.

I take the stand that with the high cost of enforcement and low stakes, CC BY SA should be interpreted as social
conventions. We comply as much as we can because it is the good citizen thing to do. But it isn't cost effective
to try to re-license everything under more compatible licenses or to fix terms of the license
that are inconvenient to comply with. The real world is messy.

Attribution
-----------
Generated libraries need to comply with Creative Commons SA licenses, up to 4 of them at the same time!

In short, code from StackOverflow must:

>- Visually indicate that the content is from Stack Overflow or the Stack Exchange network in some way. It doesn’t have to be obnoxious; a discreet text blurb is fine.
>- Hyperlink directly to the original question on the source site (e.g., http://stackoverflow.com/questions/12345)
>- Show the author names for every question and answer
>- Hyperlink each author name directly back to their user profile page on the source site (e.g., http://stackoverflow.com/users/12345/username)

[source](https://stackoverflow.blog/2009/06/25/attribution-required/)

As for so_pip:

AUTHORS,`__init__.py`, `main.py`, `CHANGELOG.txt` all have authors and links to users in some form.
`__init__.py`, `main.py` all have links to the question or answer.

If you aggressively strip out cruft, you will at least need to leave the link to the question.

Right to be forgotten
---------------------
[It looks like CC BY SA licenses says you need to remove attribution when requested](https://wiki.creativecommons.org/wiki/License_Versions#Detailed_attribution_comparison_chart)

Periodically regenerating a package, or updating it should comply.
