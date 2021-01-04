"""
Separate model for authors, licenses, maybe changelog
"""

from dataclasses import field, dataclass
from typing import List


@dataclass()
class Contribution:
    contribution_type: str = ""
    contribution_date: str = ""
    # ignore dual licenses
    contribution_license: str = ""


@dataclass()
class Author:
    id: int = 0
    emails: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)
    twitter: str = ""
    name: str = ""
    # e.g. original question, answer, question edit, answer edit, comment
    roles: List[str] = field(default_factory=list)
    contributions: List[Contribution] = field(default_factory=list)


@dataclass()
class Authors:
    """List of Authors"""

    question_id: int = 0
    answer_id: int = 0
    everyone: List[Author] = field(default_factory=list)
