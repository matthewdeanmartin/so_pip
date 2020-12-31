"""
File writing stuff
"""
import html
from typing import Dict, Any

import html2text

from so_pip.make_from_template import load_template

WINDOWS_LINE_ENDING = '\r\n'
UNIX_LINE_ENDING = '\n'


def write_as_html(
    post: Dict[str, Any], submodule_name: str
) -> None:
    """Dump post in readable form."""
    # with open(submodule_name + ".html", "w", encoding="utf-8") as diagnostics:
    #     diagnostics.write("<html><body>")
    #     diagnostics.write(post.body)
    #     diagnostics.write("</body></html>")
    template = load_template("post.html.jinja", autoescape=False)
    data = {
        "title": post.title if hasattr(post, "title") else "",
        "content": post["body"],
        "comments": post.get("comments", [])
    }
    result = template.render(item=data)
    with open(submodule_name + ".html", "w", encoding="utf-8") as diagnostics:
        diagnostics.write(result)


def write_as_text(
    post: Dict[str, Any], submodule_name: str
) -> None:
    """Dump post in readable form."""
    with open(submodule_name + ".txt", "w", encoding="utf-8") as diagnostics:
        text = html2text.html2text(post["body"])
        diagnostics.write(text)


def write_as_md(
    post: Dict[str, Any], submodule_name: str
) -> None:
    """Dump post in readable form."""
    markdown = post["body_markdown"]


    with open(submodule_name + ".md", "w", encoding="utf-8") as diagnostics:
        # https://stackoverflow.com/a/43678795/33264
        markdown = markdown.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        # don't know why it has html escapes, possibly a security feature
        # for when you know you're going to put it into HTML?
        markdown = html.unescape(markdown)
        diagnostics.write(markdown)
