"""
File writing stuff
"""
import os
from typing import Union

import html2text
import stackexchange

from so_pip.make_from_template import load_template





def write_as_html(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_name: str
) -> None:
    """Dump answer in readable form."""
    # with open(submodule_name + ".html", "w", encoding="utf-8") as diagnostics:
    #     diagnostics.write("<html><body>")
    #     diagnostics.write(post.body)
    #     diagnostics.write("</body></html>")
    template= load_template("post.html.jinja", autoescape=False)
    data = {
        "title": post.title if hasattr(post, "title") else "",
        "content":post.body,
        "comments":post.comments
    }
    result = template.render(data=data)
    with open(submodule_name + ".html", "w", encoding="utf-8") as diagnostics:
        diagnostics.write(result)


def write_as_text(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_name: str
) -> None:
    """Dump answer in readable form."""
    with open(submodule_name + ".txt", "w", encoding="utf-8") as diagnostics:
        text = html2text.html2text(post.body)
        diagnostics.write(text)


def write_as_md(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_name: str
) -> None:
    """Dump post in readable form."""
    try:
        markdown = post.body_markdown
    except AttributeError as attribute_error:
        print(attribute_error)
        return
    with open(submodule_name + ".md", "w", encoding="utf-8") as diagnostics:
        diagnostics.write(markdown)
