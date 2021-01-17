"""
Separate model for authors, licenses, maybe changelog
"""
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from so_pip.api_clients.stackapi_facade import (
    get_json_by_user_id,
    get_json_comments_by_post_id,
    get_json_revisions_by_post_id,
)
from so_pip.api_clients.stackoverflow_scraper import scrape_urls

LOGGER = logging.getLogger(__name__)


@dataclass()
class Contribution:
    """Represents what a user did"""

    contribution_type: str = ""
    contribution_date: str = ""
    # ignore dual licenses
    contribution_license: str = ""


@dataclass()
class Author:
    """Represents someone who wrote a Q, A, comment or revision"""

    author_id: int = 0
    # only if in bio!
    emails: List[str] = field(default_factory=list)
    # twitter, github, SO, homepage
    urls: List[str] = field(default_factory=list)
    homepage: str = ""
    twitter: str = ""
    github: str = ""
    display_name: str = ""
    # e.g. original question, answer, question edit, answer edit, comment
    roles: List[str] = field(default_factory=list)
    contributions: List[Contribution] = field(default_factory=list)


@dataclass()
class Authors:
    """List of Authors"""

    question_id: int = 0
    answer_id: int = 0
    everyone: List[Author] = field(default_factory=list)


def email_from_bio(bio: str) -> List[str]:
    """Rationale-- if it is not obfuscated, then they don't mind it being public"""
    # https://meta.stackexchange.com/users/98786/robert-cartaino
    matches = re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", bio)
    return matches


def normalize_user_link(url: str, user_id: int) -> str:
    """Strip off end e.g. 123/user_name"""
    return f"{url.split(str(user_id))[0]}{user_id}"


def bind_question_to_authors(question: Dict[str, Any]) -> Authors:
    """get authors for question"""
    authors = Authors()
    authors.question_id = question["question_id"]
    add_authors_from_post(question, authors, is_answer=False)
    return authors


def bind_answer_to_authors(
    answer: Dict[str, Any], question: Optional[Dict[str, Any]]
) -> Authors:
    """Get authors for post"""
    authors = Authors()
    authors.answer_id = answer["answer_id"]

    add_authors_from_post(answer, authors, is_answer=True)
    if question:
        authors.question_id = answer["question_id"]
        add_authors_from_post(answer, authors, is_answer=False)
    return authors


def add_authors_from_post(post: Dict[str, Any], authors: Authors, is_answer: bool):
    """Add authors from post to Object"""
    if post["owner"]:
        owner = Author()
        if is_answer:
            owner.roles.append("Answer Owner")
        else:
            owner.roles.append("Question Owner")
        if "user_id" in post["owner"]:
            owner.twitter, owner.github = scrape_urls(post["owner"]["user_id"])
            owner.urls.append(owner.twitter)
            owner.urls.append(owner.github)

            full_user = get_json_by_user_id(post["owner"]["user_id"])["items"][0]
            if "website_url" in full_user and full_user["website_url"]:
                owner.urls.append(full_user["website_url"])
            if "about_me" in full_user and full_user["about_me"]:
                emails = email_from_bio(full_user["about_me"])
                if emails:
                    owner.emails.extend(emails)
            if "display_name" in post["owner"] and post["owner"]["display_name"]:
                owner.display_name = post["owner"]["display_name"]
            else:
                owner.display_name = "Name not available"
        else:
            owner.display_name = "Name not available"

        if "link" in post["owner"] and post["owner"]["link"]:
            url = normalize_user_link(post["owner"]["link"], post["owner"]["user_id"])
            owner.urls.append(url)
        authors.everyone.append(owner)
    else:
        if post["user"]["user_type"] != "does_not_exist":
            LOGGER.debug("What sort of user is this?")

    post_id_name = "answer_id" if is_answer else "question_id"
    revision_json = get_json_revisions_by_post_id(post[post_id_name])
    for revision in revision_json.get("items", []):
        if revision["user"]["user_type"] == "does_not_exist":
            continue
        reviser = Author()
        if is_answer:
            reviser.roles.append("Answer Reviser")
        else:
            reviser.roles.append("Question Reviser")
        if "display_name" in revision["user"] and revision["user"]["display_name"]:
            reviser.display_name = revision["user"]["display_name"]
        else:
            reviser.display_name = "Name not available"
        full_user = get_json_by_user_id(revision["user"]["user_id"])["items"][0]
        if "website_url" in full_user and full_user["website_url"]:
            reviser.urls.append(full_user["website_url"])
        if "about_me" in full_user and full_user["about_me"]:
            reviser.emails.extend(email_from_bio(full_user["about_me"]))
        if "link" in post["owner"] and post["owner"]["link"]:
            url = normalize_user_link(
                revision["user"]["link"], revision["user"]["user_id"]
            )
            reviser.urls.append(url)

        authors.everyone.append(reviser)
    comments = get_json_comments_by_post_id(post[post_id_name])
    for comment in comments.get("items", []):
        if comment["owner"]["user_type"] == "does_not_exist":
            continue
        commenter = Author()
        if is_answer:
            commenter.roles.append("Answer Commenter")
        else:
            commenter.roles.append("Question Commenter")
        if "display_name" in comment["owner"] and comment["owner"]["display_name"]:
            commenter.display_name = comment["owner"]["display_name"]
        else:
            commenter.display_name = "Name not available"
        full_user = get_json_by_user_id(comment["owner"]["user_id"])["items"][0]
        if "website_url" in full_user and full_user["website_url"]:
            commenter.urls.append(full_user["website_url"])
        if "about_me" in full_user and full_user["about_me"]:
            commenter.emails.extend(email_from_bio(full_user["about_me"]))
        if "link" in comment["owner"] and comment["owner"]["link"]:
            url = comment["owner"]["link"]
            link = normalize_user_link(url, comment["owner"]["user_id"])
            commenter.urls.append(link)
        authors.everyone.append(commenter)
