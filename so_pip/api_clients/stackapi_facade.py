"""
Low level access. Makes no effort to parse results.
"""

import os

from stackapi import StackAPI

from so_pip import settings as settings

SITE = StackAPI("stackoverflow", key=os.environ["key"])


def get_json_by_question_id(question_id: int):
    return SITE.fetch(
        "questions/{ids}",
        ids=[
            question_id,
        ],
    )


def get_json_by_answer_id(answer_id: int):
    return SITE.fetch(
        "answers/{ids}",
        ids=[
            answer_id,
        ],
    )


def get_json_by_user_id(user_id: int):
    return SITE.fetch(
        "users/{ids}",
        ids=[
            user_id,
        ],
    )


# /2.2/posts/26344315/revisions?site=stackoverflow
def get_json_revisions_by_post_id(post_id: int):
    return SITE.fetch(
        "posts/{ids}/revisions",
        ids=[
            post_id,
        ],
    )


if __name__ == "__main__":
    a = get_json_by_answer_id(26344315)
    print(a)
    q = get_json_by_question_id(9733638)
    print(q)
