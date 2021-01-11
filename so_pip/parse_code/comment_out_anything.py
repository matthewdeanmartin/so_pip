""""
Add safe comments symbols to any list of string
"""

EXTENSION_TO_SYMBOL = {
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
    "lua": [".lua", "//"],
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


def comment_lines(code: str, language: str) -> str:
    """Add comments for any language in a naive way."""
    lines = code.split("\n")
    if language != "." and "." in language:
        extension = language.lower().split(".")[1]
        # TODO: this a waste of cpu but still probably quick
        for _, value in EXTENSION_TO_SYMBOL.items():
            if extension == value[0]:
                symbol = value[1]
    else:
        symbol = EXTENSION_TO_SYMBOL.get(language, ["", ""])[1]
    return symbol.join(lines)
