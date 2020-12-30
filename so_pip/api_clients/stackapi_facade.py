"""
Low level access. Makes no effort to parse results.
"""

import os
from typing import Any, Dict

from stackapi import StackAPI

SITE = StackAPI("stackoverflow", key=os.environ["key"])


def get_json_by_question_id(question_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return SITE.fetch(
        "questions/{ids}",
        ids=[
            question_id,
        ],
        # magic string to return more fields
        #       !9_bDDx5Ia
        # answers
        # comments
        # body
        # body_markdown
        # tags
        filter="!--1nZwHGSSZl"
    )


def get_json_by_answer_id(answer_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return SITE.fetch(
        "answers/{ids}",
        ids=[
            answer_id,
        ],
        # magic string to include certain fields.
        # need:
        #   link
        #   body_markdown
        #   body
        #   comments
        #   tags (of q)
        #   title (of q)
        filter="!3zl2.DbpKHRASLD)i"
    )


def get_json_by_user_id(user_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return SITE.fetch(
        "users/{ids}",
        ids=[
            user_id,
        ],
    )


# /2.2/posts/26344315/revisions?site=stackoverflow
def get_json_revisions_by_post_id(post_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return SITE.fetch(
        "posts/{ids}/revisions",
        ids=[
            post_id,
        ],
    )

def get_json_comments_by_post_id(post_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return SITE.fetch(
        "posts/{ids}/comments",
        ids=[
            post_id,
        ],
    )
