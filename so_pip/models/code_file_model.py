"""
Abstract model of the package_info I'm extracting from an post.
"""
from dataclasses import dataclass, field
from typing import List

from so_pip.api_clients.what_that_code_facade import guess_language_and_extension
from so_pip.models.code_block_model import CodeBlock
from so_pip.parse_code.comment_out_anything import html_to_comments
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
                items.append(html_to_comments(block.header_comments, block.language))
            if block.code_text:
                items.append(block.code_text)
            if block.footer_comments:
                items.append(html_to_comments(block.footer_comments, block.language))
        if self.code_blocks and not items:
            raise TypeError("We have code blocks, but no lines of code?")
        return items

    def all_code(self) -> List[str]:
        """Just code"""
        return [block.code_text for block in self.code_blocks]

    def all_non_code(self) -> List[str]:
        """Just non code"""
        return [block.header_comments for block in self.code_blocks] + [
            block.footer_comments for block in self.code_blocks
        ]

    def non_comment_lines(self) -> int:
        """Count code lines"""
        return sum(1 for x in self.all_code() if len(x) and not x.startswith("#"))

    def preview_final_code(self) -> str:
        """For checking if a word is in the code for an post"""
        return "\n".join(self.all_code())

    def preview_non_code(self) -> str:
        """Looking for clues about what the code language is"""
        return "\n".join(self.all_non_code())

    def analyze(self, tags: List[str]) -> None:
        """Do expensive checks"""
        final_code = self.preview_final_code()
        final_context = self.preview_non_code()

        self.is_valid_python, self.errors = validate_python(final_code)

        pair = guess_language_and_extension(
            final_code, surrounding_text=final_context, tags=tags
        )
        self.extension, self.language = pair
        if not self.extension:
            self.extension = ".wtf"
