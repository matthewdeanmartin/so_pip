"""
Generate a CHANGELOG type file based on the edit log in SO
"""
import time
from typing import Dict, Sequence, Union, Any

from so_pip.api_clients.stackapi_facade import get_json_revisions_by_post_id
from so_pip.make_from_template import load_template
from so_pip.support_files.authors import normalize_user_link


def changelog_for_post(
    post: Dict[str,Any], package_folder: str
) -> None:
    """Requirements for running `safety`"""
    versions = []
    post_id = post["answer_id"] if "answer_id" in post else post["question_id"]
    revision_json = get_json_revisions_by_post_id(post_id)
    if len(revision_json.get("items", [])) <= 1:
        return
    for revision in revision_json.get("items", []):
        # if "content_license" not in revision:
        #     print("but why")
        if "revision_number" not in revision:
            # happens with protected posts
            # no revision number, no version number
            continue
        version = {
            "version": f"0.1.{revision['revision_number']}",
            "date": f"{time.ctime(revision['creation_date'])}",
            "changes": {"content_license": revision.get("content_license", "")},
        }
        if revision["user"]["user_type"] != "does_not_exist":
            display_name = revision["user"]["display_name"]
            url = revision["user"]["link"]
            link = normalize_user_link(url, revision["user"]["user_id"])
            version["changes"]["user"] = f"{display_name} <{link}>"
        else:
            version["changes"]["user"] = "No user."
        version["changes"]["comment"] = revision.get("comment", "")
        versions.append(version)

    with open(
        package_folder + "/CHANGELOG.txt", "w", encoding="utf-8", errors="replace"
    ) as log:

        log.write(render_change_log(data=versions))


def render_change_log(
    data: Dict[str, Union[str, Sequence[str]]],
) -> str:
    """
    Render minimal setup.py suitable for `pip install -e .`
    """
    template = load_template(template_filename="HISTORY.rst.jinja", autoescape=False)
    output_text = template.render(item=data)
    return output_text
