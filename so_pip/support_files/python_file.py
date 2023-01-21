"""
Generate a python file
"""
from typing import Any, Dict

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import CodePackage
from so_pip.parse_python.format_code import format_python_file


def make_python_file(
    file_name: str,
    long_header: bool,
    code: str,
    python_submodule: CodePackage,
) -> bool:
    """write file"""
    if not python_submodule.url:
        raise TypeError("Missing post url")
    with open(file_name, "w", encoding="utf-8", errors="replace") as readme:
        data = {
            "title": python_submodule.title,
            "version": python_submodule.version,
            "post_url": python_submodule.url,
            "author": python_submodule.author,
            "author_link": python_submodule.author,
            "license": python_submodule.content_license,
            "link": python_submodule.url,
            "creation_date": python_submodule.creation_date,
            "code": code,
        }
        source = render_code_file_py(long_header, data)
        formatted_source = format_python_file(source)
        readme.write(formatted_source)
    return True


def render_code_file_py(
    long_header: bool,
    data: Dict[str, Any],
) -> str:
    """
    Rehash other stuff and act as table of contents
    """
    if long_header:
        template_filename = "python/python_long_header.py.jinja"
    else:
        template_filename = "python/python_brief_header.py.jinja"
    template = load_template(template_filename=template_filename, autoescape=False)
    # Turn off autoescape because this is python not html.
    if not data["post_url"]:
        raise TypeError("missing post+url")
    output_text = template.render(data=data, autoescape=False)  # nosec
    return output_text
