"""
Clean up the code
"""
import html2text
from bs4 import BeautifulSoup


def fix_shell(code: str) -> str:
    """Strip out >>>  and output (lines without >>>)"""
    lines = code.split("\n")
    good_lines = []
    for line in lines:
        if line.strip().startswith("$ "):
            good_lines.append("# " + line)
            continue
        good_lines.append(line)
    return "\n".join(good_lines)


def fix_interactive(code: str) -> str:
    """Strip out >>>  and output (lines without >>>)"""
    lines = code.split("\n")
    good_lines = []

    #
    interactive = sum(1 for line in lines if ">>>" in line)

    for line in lines:
        if line.startswith("... "):
            good_lines.append(line.strip()[4:])
            continue
        if line.strip() == "...":
            good_lines.append("")
            continue
        if line.strip().startswith(">>> "):
            good_lines.append(line.strip()[4:])
            continue
        if line.strip() == ">>>":
            good_lines.append("")
            continue
        # e.g. output <class xyz>
        if line.startswith("<"):
            good_lines.append("# " + str(line))
            continue
        # e.g shell output
        if line.startswith(">"):
            good_lines.append("# " + str(line))
            continue
        # e.g shell output
        if line.startswith(">> "):
            good_lines.append("# " + str(line))
            continue
        new_line = "# " + line if interactive else line
        good_lines.append(new_line)

    return "\n".join(good_lines)


def wrap_with_run(code: str) -> str:
    """Wrap with a run so it is a function, not a 'script'"""
    lines = code.split("\n")
    good_lines = ["def run() -> None:"]
    for line in lines:
        good_lines.append("    " + line)
    return "\n".join(good_lines)


def html_to_python_comments(html: str) -> str:
    """Convert HTML to python comments"""
    soup = BeautifulSoup(html, features="html.parser")
    check_if_blank = soup.get_text()
    if check_if_blank.isspace():
        # black will add space if we need it
        return ""

    # textwrap.wrap makes a mess
    # black does not re-format overlong comment lines.
    # textwrap.wrap(text, replace_whitespace=False)
    text = html2text.html2text(str(soup))
    text = text.strip(" \n")
    comment = "# " + "\n# ".join(text.split("\n"))
    return comment
