from so_pip.api_clients.pypstats_facade import find_modules
from so_pip.api_clients.pystackexchange_facade import question_by_id


def test_pystats():
    found, not_found = find_modules(
        ["module1", "module2", "motorbike", "bingo", "com.stackoverflow"], 205
    )
    assert found
    assert not_found

    found, not_found = find_modules([
        "requests",
        "compiler",
        "str",
        "boto3",
        "jiggle_version",
        "asdfasdf",
        "kaslkjasdkflajslfkjlskdjflksjflkjsaldkfj",
    ], 250, )
    assert found
    assert not_found


def test_question_by_id():
    value = question_by_id(24139250)
    assert value
