from unittest.mock import mock_open, patch

from so_pip.support_files.changelog import changelog_for_post
import so_pip.api_clients.stackapi_facade as stackapi_client
import tempfile

def test_changelog_for_post():
    answer_data = stackapi_client.get_json_by_answer_id(2572654)
    answer = answer_data["items"][0]
    with tempfile.TemporaryDirectory(prefix="test_changelog") as directory:
        folder_path = directory.replace("\\", "/")
        changelog_for_post(answer, folder_path)
