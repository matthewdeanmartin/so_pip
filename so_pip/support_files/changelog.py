"""
Generate a CHANGELOG type file based on the edit log in SO

Design strategy, follow this format: https://keepachangelog.com/en/1.0.0/

Focus on changes to the question/answers *only*, not who did it.
"""
from datetime import datetime
from typing import Any, Dict, List

from so_pip.api_clients.stackapi_facade import get_json_revisions_by_post_id
from so_pip.make_from_template import load_template
from so_pip.models.authors_model import normalize_user_link
import markdown


def changelog_for_post(post: Dict[str, Any], package_folder: str) -> None:
    """Requirements for running `safety`"""
    versions = []
    post_id = post["answer_id"] if "answer_id" in post else post["question_id"]
    revision_json = get_json_revisions_by_post_id(post_id)
    # if len(revision_json.get("items", [])) == 0:
    #     return
    for revision in revision_json.get("items", []):
        # if "content_license" not in revision:
        #     print("but why")
        if "revision_number" not in revision:
            # happens with protected posts
            # no revision number, no version number
            continue
        utc_date = datetime.utcfromtimestamp(revision["creation_date"]).isoformat()

        revision_number = revision["revision_number"]
        what = "Added" if revision_number == 1 else "Changed"
        version = {
            "version": f"0.1.{revision_number}",
            "date": f"{utc_date}",
            "changes": {
                "content_license": revision.get("content_license", ""),
                "user": "",
                "comment": "Created post",
                "what": what,
            },
        }
        if revision["user"]["user_type"] != "does_not_exist":
            display_name = revision["user"]["display_name"]
            url = revision["user"]["link"]
            link = normalize_user_link(url, revision["user"]["user_id"])
            version["changes"]["user"] = f"{display_name} <{link}>"
        else:
            version["changes"]["user"] = "No user."
        if revision_number == 1:
            added = "Added answer" if "answer_id" in post else "Added Question"
            version["changes"]["comment"] = added
        else:
            version["changes"]["comment"] = revision.get("comment", "")
        version[
            "revision_url"
        ] = f"https://stackoverflow.com/revisions/{post_id}/{revision_number}"
        versions.append(version)

    with open(
        package_folder + "/CHANGELOG.md", "w", encoding="utf-8", errors="replace"
    ) as log:
        text = render_change_log(data=versions)

        # calling this to see if it is somewhat valid markdown
        _ = markdown.markdown(text)
        log.write(text)


def render_change_log(
    data: List[Dict[str, Any]],
) -> str:
    """
    Databind to jinja file
    """
    template = load_template(template_filename="HISTORY.md.jinja", autoescape=False)
    output_text = template.render(item=data)
    return output_text
