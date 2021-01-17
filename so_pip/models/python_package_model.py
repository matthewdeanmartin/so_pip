"""
Abstract model of the package_info I'm extracting from an post.
"""
import collections
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Set, Union

from so_pip.api_clients.stackapi_facade import get_json_revisions_by_post_id
from so_pip.models.code_block_model import CodeBlock
from so_pip.models.code_file_model import CodeFile

LOGGER = logging.getLogger(__name__)


@dataclass()
class PythonPackage:
    """A question or answers's code in python module format"""

    package_name: str
    description: str

    minimum_python: str = ""
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

    answer_revisions: Dict[str, Any] = field(default_factory=dict)

    def file_frequencies(self) -> collections.Counter:
        """How many of each file type?"""
        return collections.Counter([file.extension for file in self.code_files])

    def extract_metadata(self, post: Dict[str, Any]) -> None:
        """
        Add credits and license
        """
        self.brief_header = ['"""']
        self.header = ['"""']

        # try:
        author_name = post["owner"].get("display_name", "N/A").replace("'", "\\'")
        self.author = author_name
        self.author_email = post["owner"].get("link", "N/A")
        self.header.extend(
            [
                f"Author: {self.author}",
                f"Author Link: {self.author_email}",
            ]
        )
        # except stackexchange.core.StackExchangeError:
        #     # no owner?
        #     self.author = "N/A"
        #     self.author_email = "N/A"
        #     self.header.extend(["Author info missing."])
        self.url = post["link"]
        license_text = post.get("content_license", "N/A")
        self.header.extend(
            [
                f"License: {license_text}",
                f"Date: {post['creation_date']}",
                f"Answer Url: {post['link']}",
                '"""',
                "",
            ]
        )
        self.brief_header.extend(
            [
                f"{license_text} {self.author}",
                f"{post['link']}",
                '"""',
                "",
            ]
        )

        if not self.answer_revisions:
            self.answer_revisions = get_json_revisions_by_post_id(
                post.get("answer_id", post["question_id"])
            )
        if len(self.answer_revisions.get("items", [])) >= 1:

            self.version = f"0.1.{len(self.answer_revisions.get('items', []))}"
            for revision in self.answer_revisions.get("items", []):
                coauthors = set()
                if "user" in revision:
                    coauthors.add(
                        (
                            revision["user"]["display_name"],
                            revision["user"].get("user_id", -1),
                        )
                    )
        else:
            self.version = "0.1.0 # can't get revision"

        title = post["title"].replace("'", "\\'")
        # version & author described in pep 8
        if self.python_metadata and "__title__" in "".join(self.python_metadata):
            LOGGER.debug(
                "Erasing old self.python_metadata, TODO: code shouldn't get here."
            )

        creation_date = datetime.fromtimestamp(post["creation_date"])
        self.python_metadata = [
            f"__title__ = '{title}'",
            f"__version__ = '{self.version}'",
            f"__author__ = '{self.author}'",
            f"__license__ = '{post.get('content_license', 'N/A')}'",
            f"__copyright__ = 'Copyright {creation_date} by {self.author}'",
        ]
