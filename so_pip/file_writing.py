"""
File writing stuff
"""
import html
from typing import Any, Dict, List

import html2text

from so_pip.make_from_template import load_template

WINDOWS_LINE_ENDING = "\r\n"
UNIX_LINE_ENDING = "\n"


def format_comments(comments: List[Dict[str, Any]]) -> List[str]:
    """Put comments into ordinary strings"""
    comments_formatted = []
    for comment in comments:
        owner = comment["owner"].get("display_name", "(no user)")
        license_text = comment["content_license"]
        comments_formatted.append(owner + "," + license_text)
    return comments_formatted


def write_as_html(post: Dict[str, Any], submodule_name: str) -> None:
    """Dump post in readable form."""
    template = load_template("post.html.jinja", autoescape=False)
    data = {
        "title": post.get("title", ""),
        "content": post["body"],
        "comments": format_comments(post.get("comments", [])),
    }
    result = template.render(item=data)
    with open(submodule_name + ".html", "w", encoding="utf-8") as diagnostics:
        diagnostics.write(result)


def write_as_text(post: Dict[str, Any], submodule_name: str) -> None:
    """Dump post in readable form."""
    with open(submodule_name + ".txt", "w", encoding="utf-8") as diagnostics:
        text = html2text.html2text(post["body"])
        diagnostics.write(text)


def write_as_md(post: Dict[str, Any], submodule_name: str) -> None:
    """Dump post in readable form."""
    if "body_markdown" not in post:
        return

    markdown = post["body_markdown"]

    with open(submodule_name + ".md", "w", encoding="utf-8") as diagnostics:
        # https://stackoverflow.com/a/43678795/33264
        markdown = markdown.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        # don't know why it has html escapes, possibly a security feature
        # for when you know you're going to put it into HTML?
        markdown = html.unescape(markdown)
        diagnostics.write(markdown)
