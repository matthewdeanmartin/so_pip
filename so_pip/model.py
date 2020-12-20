"""
Abstract model of the submodule I'm extracting from an answer.
"""
from dataclasses import dataclass, field
from typing import List

import stackexchange


@dataclass
class PythonSubmodule:
    """A question or answers's code in python module format"""

    # name: str
    failed_parse: bool = False
    to_write: List[str] = field(default_factory=list)
    all_code: List[str] = field(default_factory=list)
    header: List[str] = field(default_factory=list)

    def non_comment_lines(self):
        """Count code lines"""
        return sum(1 for x in self.all_code if len(x) and not x.startswith("#"))

    def strip_trailing_blank(self) -> None:
        while self.to_write and self.to_write[-1].strip() in ("", "#"):
            self.to_write.pop()

        while self.all_code and self.all_code[-1].strip() in ("", "#"):
            self.all_code.pop()

    def preview_final_code(self) -> str:
        """For checking if a word is in the code for an answer"""
        return "\n".join(self.to_write)

    def handle_header(self, answer) -> None:
        """
        Add credits and license
        """
        self.header = ['"""']
        author_name = "N/A"
        try:
            author_name = answer.owner.json.get('display_name', 'N/A').replace("'","\\'")
            self.header.extend(
                [
                    f"Author: {author_name}",
                    f"Author Link: {answer.owner.json.get('link', 'N/A')}",
                ]
            )
        except stackexchange.core.StackExchangeError:
            # no owner?
            self.header.extend(["Author info missing."])
        self.header.extend(
            [
                f"License: {answer.json.get('content_license', 'N/A')}",
                f"Date: {answer.creation_date}",
                f"Answer Url: {answer.url}",
                '"""',
                "",
            ]
        )
        answer.revisions.fetch()
        if hasattr(answer, "question"):
            title = answer.question.title.replace("'","\\'")
        else:
            title = answer.title.replace("'", "\\'")
        self.header.extend([
        f"__title__ = '{title}'",
        f"__version__ = '1.0.{len(answer.revisions)-1}'",
        f"__author__ = '{author_name}'",
        f"__license__ = '{answer.json.get('content_license', 'N/A')}'",
        f"__copyright__ = 'Copyright {answer.creation_date} by {author_name}'"
        ])
