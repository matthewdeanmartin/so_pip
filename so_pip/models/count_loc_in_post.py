"""
Count lines of code with the aim to identify posts with re-usuable code.

Single lines of code or a single inline snippet is more than likely to be noise.
"""
from typing import Any, Dict

from bs4 import BeautifulSoup


def post_has_code(answer: Dict[str, Any]) -> bool:
    """Quick string check to avoid expensive parse"""
    return "<pre><code" in answer["body"] and "</code>" in answer["body"]


def count_loc(post: Dict[str, Any]) -> int:
    """
    Only the <pre><code> blocks. Inline code blocks aren't the
    strongly reusable parts.

    Actually getting a statement count requires identify the language
    parsing it and then counting. This would make this method unbearably slow
    and failure prone.
    """
    soup = BeautifulSoup(post["body"], features="html.parser")
    codes = soup.findAll("pre")
    loc_total = 0
    for code in codes:
        lines = len(code.text.strip("\n").split("\n"))
        loc_total += lines
    return loc_total
