"""
Generate a python init file
"""
from typing import Any, Dict

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import CodePackage
from so_pip.parse_python.format_code import format_python_file


def make_python_init_file(
    file_name: str,
    python_submodule: CodePackage,
) -> bool:
    """write file"""

    with open(file_name, "w", encoding="utf-8", errors="replace") as readme:
        data = {
            "title": python_submodule.title,
            "version": python_submodule.version,
            "url": python_submodule.url,
            "author": python_submodule.author,
            "author_link": python_submodule.author,
            "license": python_submodule.content_license,
            "link": python_submodule.url,
            "creation_date": python_submodule.creation_date,
        }
        source = render_python_init_file_py(data)
        formatted_source = format_python_file(source)
        readme.write(formatted_source)
    return True


def render_python_init_file_py(
    data: Dict[str, Any],
) -> str:
    """
    Jinja for init
    """
    template = load_template(template_filename="python_init.py.jinja", autoescape=False)
    # Turn off autoescape because this is python not html.
    output_text = template.render(data=data, autoescape=False)  # nosec
    return output_text
