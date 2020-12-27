"""
Abstract model of the submodule I'm extracting from an answer.
"""
from dataclasses import dataclass, field
from typing import List

from so_pip.models.code_block_model import CodeBlock
from so_pip.parse_code.language_guessing import assign_extension
from so_pip.parse_python.python_validator import validate_python


@dataclass()
class CodeFile:
    """Represents an file which has many code blocks and comments"""

    doc_string: str = ""
    file_name: str = ""
    extension: str = ""
    language: str = ""

    is_valid_python: bool = False
    errors: List[str] = field(default_factory=list)

    code_blocks: List[CodeBlock] = field(default_factory=list)

    failed_parse: bool = False

    def to_write(self) -> List[str]:
        """Lines to write, including comments"""
        if not self.code_blocks:
            raise TypeError("No blocks")
        items = []
        for block in self.code_blocks:
            if block.header_comments:
                items.append(block.header_comments)
            if block.code_text:
                items.append(block.code_text)
            if block.footer_comments:

                items.append(block.footer_comments)
        return items

    def all_code(self) -> List[str]:
        """Just code"""
        return [block.code_text for block in self.code_blocks]

    def non_comment_lines(self) -> int:
        """Count code lines"""
        return sum(1 for x in self.all_code() if len(x) and not x.startswith("#"))

    def strip_trailing_blank(self) -> None:
        """Remove extra padding that keep creeping into the text"""
        return
        # this might not be a prob with recent refactoring
        while self.to_write() and self.to_write()[-1].strip() in ("", "#"):
            self.to_write().pop()

        while self.all_code and self.all_code()[-1].strip() in ("", "#"):
            self.all_code().pop()

    def preview_final_code(self) -> str:
        """For checking if a word is in the code for an answer"""
        return "\n".join(self.all_code())

    def analyze(self) -> None:
        """Do expensive checks"""
        final_code = self.preview_final_code()

        self.is_valid_python, self.errors = validate_python(final_code)

        self.extension, self.language = assign_extension(
            final_code, self.is_valid_python
        )
        if not self.extension:
            self.extension = ".wtf"