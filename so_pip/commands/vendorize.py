"""
Install one question or post.

Vendorize because I'm not installing it to a venv.
"""

from typing import List

from so_pip.api_clients import stackapi_facade as stackapi_client
from so_pip.parse_python.post_to_code import handle_post


def import_so_answer(
    package_prefix: str, answer_id: int, output_folder: str
) -> List[str]:
    """main entry point

    package_prefix - prefix for question and post modules

    All modules will be at same tree level
    """
    packages_made: List[str] = []
    answer_data = stackapi_client.get_json_by_answer_id(answer_id)
    answer = answer_data["items"][0]

    question_id = answer["question_id"]
    question = stackapi_client.get_json_by_question_id(question_id)["items"][0]
    packages_made.extend(handle_post(output_folder, package_prefix, question, [answer]))
    return packages_made


def import_so_question(
    package_prefix: str, question_id: int, output_folder: str
) -> List[str]:
    """main entry point

    package_prefix - prefix for question and post modules

    All modules will be at same tree level
    """
    packages_made: List[str] = []
    question = stackapi_client.get_json_by_question_id(question_id)["items"][0]

    if question["answers"]:
        packages_made.extend(
            handle_post(output_folder, package_prefix, question, question["answers"])
        )
    return packages_made
