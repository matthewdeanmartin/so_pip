"""
Authors file

This is roughly following Gnu Gnit's conventions.

Also draws inspiration from google's format.
https://opensource.google/docs/releasing/authors/

Also draws inspiration from libraries that attempt to parse AUTHORS files.
https://www.npmjs.com/package/stringify-author
https://www.npmjs.com/package/author-regex
"""

from typing import Collection, Dict, Optional, Sequence, Set, Union, Any

from so_pip.api_clients.stackapi_facade import get_json_revisions_by_post_id, \
    get_json_comments_by_post_id
from so_pip.make_from_template import load_template


def normalize_user_link(url: str, user_id: int) -> str:
    """Strip off end e.g. 123/user_name"""
    return f"{url.split(str(user_id))[0]}{user_id}"


def get_authors_for_question(question: Dict[str,Any]) -> Set[str]:
    """get authors for question"""
    authors: Set[str] = set()

    owner = question["owner"]
    link = normalize_user_link(owner["link"], owner["user_id"])
    authors.add(f"{owner['display_name']} <{link}>")

    revision_json = get_json_revisions_by_post_id(question["question_id"])
    for revision in revision_json.get("items", []):
        if revision["user"]["user_type"] == "does_not_exist":
            continue
        display_name = revision["user"]["display_name"]
        url = revision["user"]["link"]
        link = normalize_user_link(url, revision["user"]["user_id"])

        # First Last <email> (url)
        # First Last <@twitter> (url)
        authors.add(f"{display_name} <{link}>")

    # question.comments.fetch()
    # for comment in question.comments:
    #     print(comment)
    comments =get_json_comments_by_post_id(question["question_id"])
    for comment in comments.get("items",[]):
        if comment["owner"]["user_type"] == "does_not_exist":
            continue
        display_name = comment["owner"]["display_name"]
        url = comment["owner"]["link"]
        link = normalize_user_link(url, comment["owner"]["user_id"])

        # First Last <email> (url)
        # First Last <@twitter> (url)
        authors.add(f"{display_name} <{link}>")

    return authors


def get_authors_for_answer(answer: Dict[str,Any]) -> Set[str]:
    """Get authors for post"""
    authors: Set[str] = set()
    if answer["owner"]:
        owner = answer["owner"]
        if "link" not in owner:
            authors.add(f"{owner['display_name']}")
        else:
            authors.add(f"{owner['display_name']} <{owner['link']}>")
    else:
        if answer["user"]["user_type"] != "does_not_exist":
            print("What sort of user is this?")

    revision_json = get_json_revisions_by_post_id(answer["answer_id"])
    for revision in revision_json.get("items", []):
        if revision["user"]["user_type"] == "does_not_exist":
            continue
        display_name = revision["user"]["display_name"]
        url = normalize_user_link(revision["user"]["link"], revision["user"]["user_id"])
        authors.add(f"{display_name} <{url}>")

    comments =get_json_comments_by_post_id(answer["answer_id"])
    for comment in comments.get("items",[]):
        if comment["owner"]["user_type"] == "does_not_exist":
            continue
        display_name = comment["owner"]["display_name"]
        url = comment["owner"]["link"]
        link = normalize_user_link(url, comment["owner"]["user_id"])

        # First Last <email> (url)
        # First Last <@twitter> (url)
        authors.add(f"{display_name} <{link}>")

    return authors


def write_authors(
    package_folder: str,
    package_name: str,
    question: Dict[str,Any],
    answer: Optional[Dict[str,Any]] = None,
) -> None:
    """write file"""
    authors = get_authors_for_question(question)
    if answer:
        authors.union(get_authors_for_answer(answer))

    with open(
        package_folder + "/AUTHORS.txt", "w", encoding="utf-8", errors="replace"
    ) as author_file:
        item = {"name": package_name, "authors": authors}
        author_file.write(render_authors(data=item))


def render_authors(
    data: Dict[str, Union[str, Sequence[str], Collection[str]]],
) -> str:
    """
    Render minimal setup.py suitable for `pip install -e .`
    """
    template = load_template(template_filename="AUTHORS.jinja", autoescape=False)
    output_text = template.render(item=data)
    return output_text
