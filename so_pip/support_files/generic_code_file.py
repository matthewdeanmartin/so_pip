"""
Generate a python file
"""
from typing import Any, Dict

from so_pip.make_from_template import load_template


def make_generic_code_file(
    file_name: str,
    header: str,
    code: str,
    footer: str,
) -> None:
    """write file"""

    with open(file_name, "w", encoding="utf-8", errors="replace") as readme:
        data = {"header": header, "code": code, "footer": footer}
        source = render_generic_code_file(data)
        readme.write(source)


def render_generic_code_file(
    data: Dict[str, Any],
) -> str:
    """
    Just header, code, footer
    """
    template = load_template(
        template_filename="generic_code_file.jinja", autoescape=False
    )
    # Turn off autoescape because this is something, but not html.
    output_text = template.render(data=data, autoescape=False)  # nosec
    return output_text
