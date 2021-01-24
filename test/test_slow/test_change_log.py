import tempfile
import so_pip.settings as settings
from so_pip.utils.files_utils import find_file

settings.OUTPUT_FOLDER = find_file("../../output/unittest/", __file__)

import so_pip.api_clients.stackapi_facade as stackapi_client
from so_pip.support_files.changelog import changelog_for_post


def test_changelog_for_post():
    answer_data = stackapi_client.get_json_by_answer_id(2572654)
    answer = answer_data["items"][0]
    with tempfile.TemporaryDirectory(prefix="test_changelog") as directory:
        folder_path = directory.replace("\\", "/")
        changelog_for_post(answer, folder_path)
