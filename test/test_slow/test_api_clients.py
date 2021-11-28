"""
As soon as there is 1 column missing from a result, I'm lost on how to include it.
Also, this library blows up a lot.
"""

from so_pip.api_clients.pystackexchange_facade import question_by_id
import so_pip.settings as settings
from so_pip.infer_packages_needed.package_by_name import find_modules
from so_pip.utils.files_utils import find_file

settings.OUTPUT_FOLDER = find_file("../../output/unittest/", __file__)
from so_pip.api_clients.stackapi_facade import (
    get_json_by_answer_id,
    get_json_by_question_id,
)


def test_pystats():
    found, not_found = find_modules(
        ["module1", "module2", "motorbike", "bingo", "com.stackoverflow"]
    )
    assert found
    assert not_found

    found, not_found = find_modules(
        [
            "requests",
            "compiler",
            "str",
            "boto3",
            "jiggle_version",
            "asdfasdf",
            "kaslkjasdkflajslfkjlskdjflksjflkjsaldkfj",
        ],
    )
    assert found
    assert not_found

# Consistently failing on HTTPS error?!!
# def test_question_by_id():
#     value = question_by_id(24139250)
#     assert value


def test_get_json_by_answer_id():
    a = get_json_by_answer_id(26344315)
    assert a


def test_get_json_by_answer_id():
    q = get_json_by_question_id(9733638)
    assert q
