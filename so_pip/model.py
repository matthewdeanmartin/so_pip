"""
Abstract model of the submodule I'm extracting from an answer.
"""
from dataclasses import dataclass, field
from typing import List, Union

import stackexchange


@dataclass
class PythonSubmodule:
    """A question or answers's code in python module format"""

    package_name: str
    description: str
    # name: str
    failed_parse: bool = False
    to_write: List[str] = field(default_factory=list)
    all_code: List[str] = field(default_factory=list)
    header: List[str] = field(default_factory=list)
    python_metadata: List[str] = field(default_factory=list)

    version: str = ""
    url: str = ""
    author: str = ""
    author_email: str = ""
    dependencies: List[str] = field(default_factory=list)

    def non_comment_lines(self) -> int:
        """Count code lines"""
        return sum(1 for x in self.all_code if len(x) and not x.startswith("#"))

    def strip_trailing_blank(self) -> None:
        """Remove extra padding that keep creeping into the text"""
        while self.to_write and self.to_write[-1].strip() in ("", "#"):
            self.to_write.pop()

        while self.all_code and self.all_code[-1].strip() in ("", "#"):
            self.all_code.pop()

    def preview_final_code(self) -> str:
        """For checking if a word is in the code for an answer"""
        return "\n".join(self.to_write)

    def handle_header(
        self, answer: Union[stackexchange.Question, stackexchange.Answer]
    ) -> None:
        """
        Add credits and license
        """
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
        self.header.extend(
            [
                f"License: {answer.json.get('content_license', 'N/A')}",
                f"Date: {answer.creation_date}",
                f"Answer Url: {answer.url}",
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
