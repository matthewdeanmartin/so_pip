"""
Generate a python init file
"""
from typing import Any, Dict

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import CodePackage
from so_pip.parse_python.format_code import format_python_file


def make_python_init_file(
    file_name: str,
    code_info: CodePackage,
) -> bool:
    """write file"""
    is_python = any(_.language == "python" for _ in code_info.code_blocks)
    if not is_python:
        return False

    with open(file_name, "w", encoding="utf-8", errors="replace") as readme:
        data = {
            "title": code_info.title,
            "version": code_info.version,
            "url": code_info.url,
            "author": code_info.author,
            "author_link": code_info.author,
            "license": code_info.content_license,
            "link": code_info.url,
            "creation_date": code_info.creation_date,
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
    template = load_template(
        template_filename="python/python_init.py.jinja", autoescape=False
    )
    # Turn off autoescape because this is python not html.
    output_text = template.render(data=data, autoescape=False)  # nosec
    return output_text
