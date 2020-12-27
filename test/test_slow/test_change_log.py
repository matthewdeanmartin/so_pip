from unittest.mock import mock_open, patch

from so_pip.support_files.changelog import changelog_for_post
import so_pip.api_clients.pystackexchange_facade as pse
import tempfile
def test_changelog_for_post():
    answer = pse.answer_by_id(2572654)
    with tempfile.TemporaryDirectory(prefix="test_changelog") as directory:
        folder_path = directory.replace("\\", "/")
        changelog_for_post(answer, folder_path)
