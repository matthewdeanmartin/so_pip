"""
Create pyproject.toml file

Supports:
- python version from either minver or so_pip.ini
- list of inferred dependencies
- list of tags
"""
import json
import logging
from typing import Any, Dict, Optional

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import CodePackage

LOGGER = logging.getLogger(__name__)


def create_package_json(
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

    output_text = render_package_json(data)

    if not output_text:
        raise TypeError("Expected output_text by now")
    with open(
        package_folder + "/package.json", "w", encoding="utf-8", errors="replace"
    ) as project_file:
        project_file.write(output_text)
        # see if it is valid toml
        # pylint: disable=broad-except
        # noinspection PyBroadException
        try:
            json.loads(output_text)
        except BaseException as exception:
            LOGGER.error("parse failed " + str(exception))
            raise


def render_package_json(
    data: Dict[str, Any],
) -> str:
    """
    Help the world get away from setup.py
    """
    template = load_template(
        template_filename="js/package.json.jinja", autoescape=False
    )
    # Turn off autoescape because this is python not html.
    output_text = template.render(data=data, autoescape=False)  # nosec
    # validate toml
    _ = json.loads(output_text)
    return output_text
