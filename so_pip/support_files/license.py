"""
Add LICENSE file
"""
import shutil
from typing import Union

import html2text
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
    if "2.0" in license_name or "2.5" in license_name:
        # Can't find text versions of 2.5 or 2.0
        # ref https://wiki.creativecommons.org/wiki/License%20Versions
        license_path_txt = find_file(f"../licenses/{license_name}.txt", __file__)
        convert_html_to_text(license_path.replace(".txt", ".html"), license_path_txt)

    destination_path = find_file(f"{submodule_folder}/LICENSE", __file__)

    shutil.copy(license_path, destination_path)


def convert_html_to_text(license_path: str, license_path_txt: str) -> None:
    """One time convert html to txt"""
    with open(license_path) as license_as_html:
        text = html2text.html2text(license_as_html.read())
    with open(license_path_txt, "w") as write_text:
        write_text.write(text)
