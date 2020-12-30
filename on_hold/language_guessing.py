"""
What programming language is this text
"""
from typing import Tuple

from so_pip import settings as settings
from so_pip.parse_python.detect_python import score

FILE_EXTENSIONS = {
    "Batchfile": ".bat",
    "C": ".c",
    "C#": ".cs",
    "C++": ".cpp",
    "CSS": ".css",
    "CoffeeScript": ".coffee",
    "Erlang": ".erlang",
    "Go": ".go",
    "HTML": ".html",
    "Haskell": ".haskell",
    "Java": ".java",
    "JavaScript": ".js",
    "Jupyter Notebook": ".nb",
    "Lua": ".lua",
    "Markdown": ".md",
    "Matlab": ".matlab",
    "Objective-C": ".objc",
    "PHP": ".php",
    "Perl": ".perl",
    "PowerShell": ".ps1",
    "Python": ".py",
    "R": ".r",
    "Ruby": ".rb",
    "Rust": ".rust",
    "SQL": ".sql",
    "Scala": ".scala",
    "Shell": ".sh",
    "Swift": ".swift",
    "TeX": ".tex",
    "TypeScript": ".ts",
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


def assign_extension(all_code: str, failed_parse: bool) -> Tuple[str, str]:
    """Guess language and extension"""
    if is_likely_bash(all_code):
        return (
            FILE_EXTENSIONS["Shell"],
            "Shell",
        )

    if not failed_parse:
        return FILE_EXTENSIONS["Python"], "Python"

    if not all_code:
        return FILE_EXTENSIONS[settings.DEFAULT_LANGUAGE], settings.DEFAULT_LANGUAGE

    if score(all_code) > 5:
        return FILE_EXTENSIONS["Python"], "Python"

    # pylint: disable=global-statement
    global GUESS  # noqa
    if not GUESS:
        # SLOW. Event just importing is slow
        # pylint: disable=import-outside-toplevel
        from guesslang import Guess

        GUESS = Guess()
    language = GUESS.language_name(all_code)
    if (
        "*" in settings.POSSIBLE_LANGUAGES
        and language not in settings.POSSIBLE_LANGUAGES
    ):
        language = settings.DEFAULT_LANGUAGE
    extension = FILE_EXTENSIONS.get(language, settings.DEFAULT_LANGUAGE)
    return extension, language
