"""
Packaging for lua ecosystem
"""
import logging
from typing import Any, Dict, Optional

from slpp import slpp as lua

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import CodePackage

LOGGER = logging.getLogger(__name__)


def create_rockspec(
    package_folder: str,
    code_info: CodePackage,
    question: Dict[str, Any],
    answer: Optional[Dict[str, Any]],
) -> None:
    """Put everything into setup.cfg"""
    # maybe already done?
    # post_id = answer["answer_id"] if answer else question["question_id"]
    # revisions_json = get_json_revisions_by_post_id(post_id).get("items", [])
    if answer:
        url = answer["link"]
    else:
        url = question["link"]

    data = {
        "dependencies": code_info.dependencies,
        "question_title": question["title"],
        "revision_number": code_info.version,  # or len(revisions_json)
        "name": code_info.package_name,
        "tags": question["tags"],
        "url": url,
    }

    output_text = render_lua_rockspec(data)

    if not output_text:
        raise TypeError("Expected output_text by now")
    with open(
        package_folder + f"/{code_info.package_name}-{code_info.version}.rockspec",
        "w",
        encoding="utf-8",
        errors="replace",
    ) as project_file:
        # I think the spec is lua syntax
        project_file.write(output_text)


def render_lua_rockspec(
    data: Dict[str, Any],
) -> str:
    """
    Help the world get away from setup.py
    """
    # I think the spec is lua syntax
    template = load_template(
        template_filename="lua/lua_rockspec.jinja", autoescape=False
    )

    output_text = template.render(data=data, autoescape=False)  # nosec
    # check if it parses.
    _ = lua.decode(output_text)
    return output_text
