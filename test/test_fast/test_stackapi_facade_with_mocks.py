from unittest.mock import patch

import so_pip.api_clients.stackapi_facade as stack


@patch("stackapi.StackAPI.fetch", return_value={})
def test_get_json_by_answer_id(mock):
    print(stack.get_json_by_answer_id(1))
    assert mock.called and mock.call_count == 1


@patch("stackapi.StackAPI.fetch", return_value={})
def test_get_json_by_question_id(mock):
    print(stack.get_json_by_question_id(1))
    assert mock.called and mock.call_count == 1


@patch("stackapi.StackAPI.fetch", return_value={})
def test_get_json_by_search(mock):
    print(stack.get_json_by_search("foo", ("bar", "baz")))
    assert mock.called and mock.call_count == 1


@patch("stackapi.StackAPI.fetch", return_value={})
def test_get_json_by_user_id(mock):
    print(stack.get_json_by_user_id(1))
    assert mock.called and mock.call_count == 1


@patch("stackapi.StackAPI.fetch", return_value={})
def test_get_json_revisions_by_post_id(mock):
    print(stack.get_json_revisions_by_post_id(1))
    assert mock.called and mock.call_count == 1


@patch("stackapi.StackAPI.fetch", return_value={})
def test_get_json_comments_by_post_id(mock):
    print(stack.get_json_comments_by_post_id(1))
    assert mock.called and mock.call_count == 1
