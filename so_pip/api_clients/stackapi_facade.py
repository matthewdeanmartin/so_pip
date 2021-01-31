"""
Low level access. Makes no effort to parse results.
"""
import pickle

import os
from typing import Any, Dict, Tuple, cast

from diskcache import Cache
from stackapi import StackAPI

from so_pip import settings as settings

if settings.OUTPUT_FOLDER == "":
    raise TypeError("Loaded this module too early.")
# TODO: consider moving to JsonDisk from same library
# not sure if that means python in, json out, so may have to change all client code
_CACHE = Cache(directory=settings.OUTPUT_FOLDER + f"/cache{pickle.DEFAULT_PROTOCOL}/")

if os.environ.get("key", None):
    SITE = StackAPI("stackoverflow", key=os.environ["key"])
else:
    SITE = StackAPI("stackoverflow")

CACHE_SECONDS = 86400


# @lru_cache(maxsize=1000)
@_CACHE.memoize(expire=CACHE_SECONDS)
def get_json_by_search(query: str, tagged: Tuple[str, ...]) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return cast(
        Dict[str, Any],
        SITE.fetch(
            "search?tagged={tagged}&intitle={intitle}",
            tagged=[";".join(tagged)],
            intitle=[query],
        ),
    )


# @lru_cache(maxsize=1000)
@_CACHE.memoize(expire=CACHE_SECONDS)
def get_json_by_question_id(question_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return cast(
        Dict[str, Any],
        SITE.fetch(
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
            filter="!--1nZwHGSSZl",
        ),
    )


# @lru_cache(maxsize=1000)
@_CACHE.memoize(expire=CACHE_SECONDS)
def get_json_by_answer_id(answer_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return cast(
        Dict[str, Any],
        SITE.fetch(
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
            filter="!3zl2.DbpKHRASLD)i",
        ),
    )


# @lru_cache(maxsize=1000)
@_CACHE.memoize(expire=CACHE_SECONDS)
def get_json_by_user_id(user_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return cast(
        Dict[str, Any],
        SITE.fetch(
            "users/{ids}",
            ids=[
                user_id,
            ],
            # just stuff we care about + about_me
            filter="!)si8a_4RZpJGdK21mxCq",
        ),
    )


# /2.2/posts/26344315/revisions?site=stackoverflow
# @lru_cache(maxsize=1000)
@_CACHE.memoize(expire=CACHE_SECONDS)
def get_json_revisions_by_post_id(post_id: int) -> Dict[str, Any]:
    """
    Low level access, returns unprocessed json
    A post id is a question OR an answer id!
    """
    return cast(
        Dict[str, Any],
        SITE.fetch(
            "posts/{ids}/revisions",
            ids=[
                post_id,
            ],
            filter="!9_bDDm2Bc",
        ),
    )


# @lru_cache(maxsize=1000)
@_CACHE.memoize(expire=CACHE_SECONDS)
def get_json_comments_by_post_id(post_id: int) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return cast(
        Dict[str, Any],
        SITE.fetch(
            "posts/{ids}/comments",
            ids=[
                post_id,
            ],
            # need comment body & body_md, link
            filter="!--1nZxT00Un.",
        ),
    )


# @lru_cache(maxsize=1000)
@_CACHE.memoize(expire=CACHE_SECONDS)
def get_json_related_tags(tag: str) -> Dict[str, Any]:
    """Low level access, returns unprocessed json"""
    return cast(
        Dict[str, Any],
        SITE.fetch(
            "tags/{ids}/related",
            ids=[
                tag,
            ],
        ),
    )
