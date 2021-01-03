"""
Abstract model of the package_info I'm extracting from an post.
"""
from dataclasses import dataclass, field
from typing import List

from so_pip.language_guessing.language_guessing import assign_extension
from so_pip.parse_python.python_validator import validate_python


@dataclass()
class CodeBlock:
    """Represents an html code block"""

    # raw text, straight from the MD/HTML
    raw_text: str = ""
    # Cleaned up source code
    code_text: str = ""
    # English code that will need to be commented out
    header_comments: str = ""
    footer_comments: str = ""
    # If not, could still be bad python or English or some other language
    is_valid_python: bool = False
    errors: List[str] = field(default_factory=list)
    is_python_error_message: bool = False
    is_interactive_block: bool = False
    is_ipython_block: bool = False
    starts_new_file: bool = False
    extension: str = ""
    language: str = ""

    def analyze(self, tags: List[str]) -> None:
        """Do expensive checks"""
        self.is_ipython_block = ">>>" in self.code_text
        self.is_valid_python, self.errors = validate_python(self.code_text)

        value = assign_extension(self.code_text, tags)
        self.extension, self.language = value
