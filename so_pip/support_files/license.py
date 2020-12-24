"""
Add LICENSE file
"""
import shutil
from typing import Union

import stackexchange

from so_pip.file_writing import find_file


def write_license(
    post: Union[stackexchange.Question, stackexchange.Answer], submodule_folder: str
) -> None:
    """Include license file
    Each revision could have different license!
    """
    license_name = post.json.get("content_license", "N/A")
    if license_name == "N/A":
        print(post.json)
        return
    license_path = find_file(f"../licenses/{license_name}.txt", __file__)
    destination_path = find_file(f"{submodule_folder}/LICENSE", __file__)

    shutil.copy(license_path, destination_path)
