"""
Handle a single code block of any language.

I don't really want to support all languages, but even python questions often
involve a bit of shell script, python, c, and other things.
"""
import re
from typing import List

from bs4 import BeautifulSoup

from so_pip.model import CodeBlock
from so_pip.parse_python.code_transformations import fix_interactive, fix_shell


def find_code_blocks(html: str) -> List[CodeBlock]:
    """Build up code blocks of potentially many languages."""
    blocks: List[CodeBlock] = []
    regex_expression = '(<pre class="[a-z -]*"><code>|<pre><code>|</code></pre>)'
    parts = re.split(regex_expression, html)

    in_comment = True

    # split into
    #    comments (optional)
    #    code
    #    ----optional file break----
    #    comments
    #    code
    #    comments (optional)
    #
    # We are assuming all comments are headers, except degenerate cases of
    # comment/code/comment
    # and
    # code/comment
    # but for longer runs, we assume comment/code/file break
    first = True
    for part in parts:
        if part.isspace():
            continue
        if part.startswith("<pre") and part.endswith("<code>"):
            in_comment = False
            continue
        if part == "</code></pre>":
            in_comment = True
            continue
        if in_comment:
            block = CodeBlock()
            blocks.append(block)

            if first:
                block.starts_new_file = True
                first = False

            if part:
                block.header_comments = part
            continue
        if first:
            block = CodeBlock()
            blocks.append(block)
            block.starts_new_file = True
            first = False

        # handle html escapes in what is mostly not html
        soup = BeautifulSoup(
            "<pre><code>" + part + "</code></pre>", features="html.parser"
        )
        code = soup.findAll("code")[0].text

        # python shell stuff
        code = fix_interactive(code)
        # bash shell stuff
        code = fix_shell(code)

        block.code_text = code

        block.analyze()
        if block.extension == ".py" and (
            code.startswith("import ") or code.startswith("from ")
        ):
            block.starts_new_file = True
        # blocks.append(block)
        # block = None

    # handle this:
    #    text
    #    code
    #    text
    if len(blocks) >= 2:
        last = blocks[-1]
        if last.header_comments and blocks[-2].code_text:
            blocks[-2].footer_comments = last.header_comments
            blocks.pop()
    for block in blocks:
        if not block.extension:
            block.analyze()
    return blocks
