"""
What programming language is this text
"""
from typing import List, Optional, Tuple

from so_pip.parse_python.detect_python import score
from so_pip.settings import DEFAULT_LANGUAGE

FILE_EXTENSIONS = {
    "batchfile": ".bat",
    "c": ".c",
    "c#": ".cs",
    "c++": ".cpp",
    "css": ".css",
    "coffeescript": ".coffee",
    "erlang": ".erlang",
    "go": ".go",
    "html": ".html",
    "haskell": ".haskell",
    "java": ".java",
    "javascript": ".js",
    "jupyter notebook": ".nb",
    "lua": ".lua",
    "markdown": ".md",
    "matlab": ".matlab",
    "objective-C": ".objc",
    "php": ".php",
    "perl": ".perl",
    "powershell": ".ps1",
    "python": ".py",
    "r": ".r",
    "ruby": ".rb",
    "rust": ".rust",
    "sql": ".sql",
    "scala": ".scala",
    "shell": ".sh",
    "swift": ".swift",
    "tex": ".tex",
    "typescript": ".ts",
}

GUESS = None


def is_likely_bash(value: str) -> bool:
    """Likely bash"""
    parts = value.strip().split()
    if parts and parts[0] in [
        "sudo",
        "pip",
        "python",
        "python2",
        "python3",
        "apt-get",
        "yum",
    ]:
        return True
    return False


def assign_extension(
    all_code: str, failed_parse: bool, tags: List[str]
) -> Tuple[str, str]:
    """Guess language and extension"""
    if is_likely_bash(all_code):
        return (
            FILE_EXTENSIONS["shell"],
            "Shell",
        )

    if not failed_parse:
        return FILE_EXTENSIONS["python"], "python"

    if not all_code:
        return DEFAULT_LANGUAGE

    if score(all_code) > 5:
        return FILE_EXTENSIONS["python"], "python"

    # convert tag to language here.
    extension_language = match_tag_to_language(tags)
    if extension_language:
        extension, guessed_language = extension_language
        return extension, guessed_language

    return DEFAULT_LANGUAGE


def match_tag_to_language(tags: List[str]) -> Optional[Tuple[str, str]]:
    """Guess language by tag"""
    for tag in (_.lower() for _ in tags):
        if not tag:
            continue
        if tag in FILE_EXTENSIONS:
            return FILE_EXTENSIONS[tag], tag
    return None
