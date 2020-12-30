"""
Add LICENSE files

The world actually doesn't know how to handle this. Not only is an SO post under
a weird CC license, but each part could be under one of 4 different versions of
CC BY-SA!
https://softwareengineering.stackexchange.com/questions/304874/
declaring-multiple-licences-in-a-github-project

Since other tools only look at LICENSE, I'll put the "principal" one there.

"""
import shutil
from typing import List, Any, Dict

import html2text

from so_pip import settings as settings
from so_pip.api_clients.stackapi_facade import get_json_revisions_by_post_id, \
    get_json_comments_by_post_id
from so_pip.utils.files_utils import find_file


def write_license(
    post: Dict[str, Any], package_folder: str
) -> None:
    """Include license file
    Each revision could have different license!
    """
    licenses: List[str] = []
    post_license = post.get("content_license", "N/A")
    licenses.append(post_license)
    post_id = post["answer_id"] if "answer_id" in post else post["question_id"]
    revision_json = get_json_revisions_by_post_id(post_id)

    for revision in revision_json.get("items", []):
        # if revision["user"]["user_type"] == "does_not_exist":
        #     continue
        # display_name = revision["user"]["display_name"]
        # url = revision["user"]["link"]
        # link = normalize_user_link(url, revision["user"]["user_id"])
        licenses.append(revision.get("content_license", "N/A"))

    comments = get_json_comments_by_post_id(post_id)
    for comment in comments.get("items", []):
        # if comment["owner"]["user_type"] == "does_not_exist":
        #     continue
        # display_name = comment["owner"]["display_name"]
        # url = comment["owner"]["link"]
        # link = normalize_user_link(url, comment["user"]["user_id"])

        licenses.append(comment.get("content_license", "N/A"))

        # First Last <email> (url)
        # First Last <@twitter> (url)
        # authors.add(f"{display_name} <{link}>")

    for license_name in set(licenses):
        if license_name == "N/A":
            # these really happen, not sure why.
            continue
        license_path = find_file(f"../licenses/{license_name}.txt", __file__)
        # if "2.0" in license_name or "2.5" in license_name:
        #     # Can't find text versions of 2.5 or 2.0
        #     # ref https://wiki.creativecommons.org/wiki/License%20Versions
        #     license_path_txt = find_file(f"../licenses/{license_name}.txt", __file__)
        #     convert_html_to_text(license_path.replace(".txt", ".html"), license_path_txt)

        destination_path = find_file(f"{package_folder}/LICENSE",
                                     settings.TARGET_FOLDER)

        shutil.copy(license_path, destination_path)


def convert_html_to_text(license_path: str, license_path_txt: str) -> None:
    """One time convert html to txt"""
    with open(license_path) as license_as_html:
        text = html2text.html2text(license_as_html.read())
    with open(license_path_txt, "w") as write_text:
        write_text.write(text)
