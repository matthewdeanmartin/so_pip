"""
Abstract model of the submodule I'm extracting from an answer.
"""
import collections
from dataclasses import dataclass, field
from typing import List, Set, Union

import stackexchange

from so_pip.models.code_block_model import CodeBlock
from so_pip.models.code_file_model import CodeFile


@dataclass()
class PythonPackage:
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
    dependencies: Union[List[str], Set[str]] = field(default_factory=list)

    def file_frequencies(self) -> collections.Counter:
        """How many of each file type?"""
        return collections.Counter([file.extension for file in self.code_files])

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
                    # todo... handle closed accounts
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
