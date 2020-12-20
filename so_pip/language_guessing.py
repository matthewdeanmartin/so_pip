"""
What programming language is this text
"""
from typing import Tuple

from so_pip.settings import DEFAULT_LANGUAGE, POSSIBLE_LANGUAGES

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


def assign_extension(all_code: str, failed_parse: bool) -> Tuple[str, str]:
    """Guess language and extension"""
    if failed_parse:
        diagnostics_all_code = "\n".join(all_code)
        if diagnostics_all_code:
            # pylint: disable=global-statement
            global GUESS  # noqa
            if not GUESS:
                # SLOW. Event just importing is slow
                # pylint: disable=import-outside-toplevel
                from guesslang import Guess

                GUESS = Guess()
            language = GUESS.language_name(diagnostics_all_code)
            if language not in POSSIBLE_LANGUAGES:
                language = DEFAULT_LANGUAGE
        else:
            language = DEFAULT_LANGUAGE
    else:
        language = DEFAULT_LANGUAGE
    extension = FILE_EXTENSIONS.get(language, DEFAULT_LANGUAGE)
    return extension, language
