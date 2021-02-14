""""
Add safe comments symbols to any list of string
"""
import html2text
from bs4 import BeautifulSoup

from so_pip.parse_python.code_transformations import html_to_python_comments

LANGUAGE_TO_SYMBOL = {
    "batchfile": [".bat", "REM"],
    "c": [".c", "//"],
    "c#": [".cs", "//"],
    "c++": [".cpp", "//"],
    "css": [".css", "//"],
    "coffeescript": [".coffee", "//"],
    "erlang": [".erlang", "//"],
    "go": [".go", "//"],
    "html": [".html", ""],
    "haskell": [".haskell", "//"],
    "java": [".java", "//"],
    "javascript": [".js", "//"],
    "jupyter notebook": [".nb", ""],
    "lua": [".lua", "--"],
    "markdown": [".md", ""],
    "matlab": [".matlab", "//"],
    "objective-C": [".objc", "//"],
    "php": [".php", "//"],
    "perl": [".perl", "//"],
    "powershell": [".ps1", "#"],
    "python": [".py", "#"],
    "r": [".r", "#"],
    "ruby": [".rb", "#"],
    "rust": [".rust", "//"],
    "sql": [".sql", "--"],
    "scala": [".scala", "//"],
    "shell": [".sh", "#"],
    "swift": [".swift", "//"],
    "tex": [".tex", "//"],
    "typescript": [".ts", "//"],
}


def html_to_comments(html: str, language: str) -> str:
    """Convert html to text and comment it out according to
    line by line comment syntax for language"""
    if language in ("python", ".py"):
        return html_to_python_comments(html)

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
    return comment_lines(text, language)


def comment_lines(code: str, language: str) -> str:
    """Add comments for any language in a naive way."""
    lines = code.split("\n")
    symbol = "//"
    if language != "." and "." in language:
        extension = language.lower().split(".")[1]
        # TODO: this a waste of cpu but still probably quick
        for _, value in LANGUAGE_TO_SYMBOL.items():
            if extension == value[0]:
                symbol = value[1]
    else:
        symbol = LANGUAGE_TO_SYMBOL.get(language, ["", ""])[1]

    lines = [symbol + " " + line for line in lines]
    return "\n".join(lines)
