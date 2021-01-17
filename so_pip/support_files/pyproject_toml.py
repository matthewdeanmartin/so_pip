"""
Create pyproject.toml file

Supports:
- python version from either minver or so_pip.ini
- list of inferred dependencies
- list of tags
"""
import logging
from typing import Any, Dict, Optional

import toml

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import PythonPackage
import toml

LOGGER = logging.getLogger(__name__)


def create_pytroject_toml(
    package_folder: str,
    python_submodule: PythonPackage,
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
        "dependencies": python_submodule.dependencies,
        "question_title": question["title"],
        "revision_number": python_submodule.version,  # or len(revisions_json)
        "minimum_python": python_submodule.minimum_python,
        "name": python_submodule.package_name,
        "tags": question["tags"],
        "url": url,
    }

    output_text = render_pyproject_toml(data)

    if not output_text:
        raise TypeError("Expected output_text by now")
    with open(
        package_folder + "/pyproject.toml", "w", encoding="utf-8", errors="replace"
    ) as project_file:
        project_file.write(output_text)
        # see if it is valid toml
        # pylint: disable=broad-except
        # noinspection PyBroadException
        try:
            toml.loads(output_text)
        except BaseException as exception:
            LOGGER.error("parse failed " + str(exception))
            raise


def render_pyproject_toml(
    data: Dict[str, Any],
) -> str:
    """
    Help the world get away from setup.py
    """
    template = load_template(template_filename="pyproject.toml.jinja", autoescape=False)
    # Turn off autoescape because this is python not html.
    output_text = template.render(data=data, autoescape=False)  # nosec
    # validate toml
    _ = toml.loads(output_text)
    return output_text
