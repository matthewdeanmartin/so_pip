"""
Abstract model of the package_info I'm extracting from an post.
"""
import collections
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Sequence

from so_pip.models.code_block_model import CodeBlock
from so_pip.models.code_file_model import CodeFile

LOGGER = logging.getLogger(__name__)


@dataclass()
class CodePackage:
    """A question or answers's code in python module format"""

    package_name: str
    description: str

    minimum_python: str = ""
    brief_header: List[str] = field(default_factory=list)

    code_files: List[CodeFile] = field(default_factory=list)
    header: List[str] = field(default_factory=list)

    # python_metadata: List[str] = field(default_factory=list)
    code_blocks: List[CodeBlock] = field(default_factory=list)

    content_license: str = ""
    title: str = ""
    creation_date: str = ""
    version: str = ""
    url: str = ""
    author: str = ""
    author_email: str = ""
    coauthors: Sequence[str] = field(default_factory=list)
    dependencies: Sequence[str] = field(default_factory=list)

    answer_revisions: Dict[str, Any] = field(default_factory=dict)

    def file_frequencies(self) -> collections.Counter:
        """How many of each file type?"""
        return collections.Counter([file.extension for file in self.code_files])

    def extract_metadata(self, post: Dict[str, Any]) -> None:
        """
        Add credits and license
        """

        author_name = (
            post["owner"]
            .get("display_name", "Author name not available")
            .replace("'", "\\'")
        )
        self.author = author_name
        self.author_email = post["owner"].get("link", "Author link not available")
        self.url = post["link"]
        self.content_license = post.get(
            "content_license", "CC-BY-SA, exact version not specified"
        )

        if not self.answer_revisions:
            # pylint: disable=import-outside-toplevel
            from so_pip.api_clients.stackapi_facade import get_json_revisions_by_post_id

            self.answer_revisions = get_json_revisions_by_post_id(
                post.get("answer_id", post["question_id"])
            )
        if len(self.answer_revisions.get("items", [])) >= 1:
            self.version = f"0.1.{len(self.answer_revisions.get('items', []))}"
        else:
            self.version = "0.1.0 # can't get revision"

        self.title = post["title"].replace("'", "\\'")

        self.creation_date = str(datetime.fromtimestamp(post["creation_date"]))
