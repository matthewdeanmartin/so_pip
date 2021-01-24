import tempfile

import so_pip.settings as settings
from so_pip.utils.files_utils import find_file

settings.OUTPUT_FOLDER = find_file("../../output/unittest/", __file__)

import so_pip.api_clients.stackapi_facade as stackapi_client

# from so_pip.support_files.authors import (
#     get_authors_for_answer,
#     get_authors_for_question,
# )
from so_pip.support_files.authors import write_authors


def test_write_authors():
    data = stackapi_client.get_json_by_question_id(9733638)
    q = data["items"][0]
    answer_data = stackapi_client.get_json_by_answer_id(26344315)
    a = answer_data["items"][0]
    with tempfile.TemporaryDirectory(prefix="test_authors") as directory:
        folder_path = directory.replace("\\", "/")
        write_authors(folder_path, "foobar", q, a)


# def test_authors_with_comments():
#     data = stackapi_client.get_json_by_question_id(55019378)
#     q = data["items"][0]
#     authors = get_authors_for_question(q)
#     assert authors
#
#
# def test_authors():
#     data = stackapi_client.get_json_by_question_id(9733638)
#     q = data["items"][0]
#     answer_data = stackapi_client.get_json_by_answer_id(26344315)
#     a = answer_data["items"][0]
#     authors = get_authors_for_question(q)
#     assert authors
#     more_authors = get_authors_for_answer(a)
#     assert more_authors
