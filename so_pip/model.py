"""
Abstract model of the submodule I'm extracting from an answer.
"""
from dataclasses import dataclass, field
from typing import List, Union

import stackexchange

from so_pip.parse_code.language_guessing import assign_extension
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

    def analyze(self) -> None:
        """Do expensive checks"""
        self.is_ipython_block = ">>>" in self.code_text
        self.is_valid_python, self.errors = validate_python(self.code_text)

        self.extension, self.language = assign_extension(
            self.code_text, self.is_valid_python
        )


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


@dataclass()
class PythonSubmodule:
    """A question or answers's code in python module format"""

    package_name: str
    description: str
    # name: str
    brief_header: List[str] = field(default_factory=list)

    code_files: List[CodeFile] = field(default_factory=list)
    header: List[str] = field(default_factory=list)

    python_metadata: List[str] = field(default_factory=list)
    code_blocks: List[CodeBlock] = field(default_factory=list)

    version: str = ""
    url: str = ""
    author: str = ""
    author_email: str = ""
    dependencies: List[str] = field(default_factory=list)

    def extract_metadata(
        self, answer: Union[stackexchange.Question, stackexchange.Answer]
    ) -> None:
        """
        Add credits and license
        """
        self.brief_header = ['"""']
        self.header = ['"""']

        try:
            author_name = answer.owner.json.get("display_name", "N/A").replace(
                "'", "\\'"
            )
            self.author = author_name
            self.author_email = answer.owner.json.get("link", "N/A")
            self.header.extend(
                [
                    f"Author: {self.author}",
                    f"Author Link: {self.author_email}",
                ]
            )
        except stackexchange.core.StackExchangeError:
            # no owner?
            self.author = "N/A"
            self.author_email = "N/A"
            self.header.extend(["Author info missing."])
        self.url = answer.url
        license_text = answer.json.get("content_license", "N/A")
        self.header.extend(
            [
                f"License: {license_text}",
                f"Date: {answer.creation_date}",
                f"Answer Url: {answer.url}",
                '"""',
                "",
            ]
        )
        self.brief_header.extend(
            [
                f"{license_text} {self.author}",
                f"{answer.url}",
                '"""',
                "",
            ]
        )

        try:
            answer.revisions.fetch()
            self.version = f"1.0.{len(answer.revisions) - 1}"
            coauthors = set()
            if len(answer.revisions) > 1:
                for revision in answer.revisions:
                    # todo... handle closed accts
                    coauthors.add((revision.user.display_name, revision.user.id))
            if len(coauthors) > 1:
                print(coauthors)
        except KeyError:
            # bug in client, fails when user no longer exists/user_id missing
            self.version = "0.1.0 # can't get revision"

        if hasattr(answer, "question"):
            title = answer.question.title.replace("'", "\\'")
        else:
            title = answer.title.replace("'", "\\'")
        # version & author described in pep 8
        self.python_metadata.extend(
            [
                f"__title__ = '{title}'",
                f"__version__ = '{self.version}'",
                f"__author__ = '{self.author}'",
                f"__license__ = '{answer.json.get('content_license', 'N/A')}'",
                f"__copyright__ = 'Copyright {answer.creation_date} by {self.author}'",
            ]
        )
