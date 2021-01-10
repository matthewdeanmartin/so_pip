"""
Install one question or post.

Vendorize because I'm not installing it to a venv.
"""

from typing import List, Optional

from so_pip.api_clients import stackapi_facade as stackapi_client
from so_pip.parse_python.post_to_code import handle_post
from so_pip.utils import guards as guards
from so_pip.utils.user_trace import inform


def import_so_answer(
    package_prefix: str, answer_id: int, output_folder: str, revision_id: Optional[int]
) -> List[str]:
    """main entry point

    package_prefix - prefix for question and post modules

    All modules will be at same tree level
    """
    guards.must_be_truthy(output_folder, "output_folder required")
    guards.must_be_truthy(answer_id, "answer_id required")
    inform(f"Importing answer #'{answer_id}'...")
    if not package_prefix:
        package_prefix = ""
    packages_made: List[str] = []
    answer_data = stackapi_client.get_json_by_answer_id(answer_id)
    if not answer_data["items"]:
        raise TypeError("Answer not found, maybe this is a question id?")
    answer = answer_data["items"][0]

    if revision_id and revision_id > 0:
        revisions = stackapi_client.get_json_revisions_by_post_id(answer_id)
        for item in revisions["items"]:
            # some revisions are not "real" revisions and have no number
            if item.get("revision_number", -1) == revision_id:
                revision = item
    else:
        revision = None

    question_id = answer["question_id"]
    question = stackapi_client.get_json_by_question_id(question_id)["items"][0]
    packages_made.extend(
        handle_post(output_folder, package_prefix, question, [answer], revision)
    )
    return packages_made


def import_so_question(
    package_prefix: str, question_id: int, output_folder: str
) -> List[str]:
    """main entry point

    package_prefix - prefix for question and post modules

    All modules will be at same tree level
    """
    inform(f"Importing question #'{question_id}'...")
    packages_made: List[str] = []
    question = stackapi_client.get_json_by_question_id(question_id)["items"][0]

    if question["answers"]:
        packages_made.extend(
            handle_post(output_folder, package_prefix, question, question["answers"])
        )
    return packages_made
