"""
Wrapper around pystackexchange, mostly to cope with bugs without fully vendorizing

Basic object fetching works fine, but attributes can be missing, or errors thrown
when attributes aren't as expected.
"""
import os
from typing import List

import stackexchange

STACK = stackexchange.Site(stackexchange.StackOverflow, os.environ["key"])


def question_by_id(question_id: int) -> stackexchange.Question:
    """Get question object graph"""
    if not question_id:
        raise TypeError("question_id is required")
    STACK.include_body = True
    question = STACK.question(question_id)
    return question


def answer_by_id(answer_id: int) -> stackexchange.Question:
    """Get answer object graph"""
    if not answer_id:
        raise TypeError("answer_id is required")
    STACK.include_body = True
    answer = STACK.answer(answer_id)
    return answer


def user_by_id(user_id: int) -> stackexchange.Question:
    """Get question object graph"""
    if not user_id:
        raise TypeError("user_id is required")
    STACK.include_body = True
    user = STACK.user(user_id)
    return user


def python_questions(search: str) -> List[stackexchange.Question]:
    """Get some questions and answers by keyword"""
    suitable = []
    print(f"TODO: search {search}")
    for question in STACK.questions(tagged=["python"], pagesize=10):
        suitable.append(question)
    return suitable
