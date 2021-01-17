"""
Rehash some fairly non-standardized stuff about the package
"""
from typing import Any, Dict, Optional

import markdown

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import PythonPackage


def create_readme_md(
    package_folder: str,
    python_submodule: PythonPackage,
    question: Dict[str, Any],
    answer: Optional[Dict[str, Any]] = None,
) -> None:
    """write file"""

    # TODO: this isn't done yet.
    print(answer)
    with open(
        package_folder + "/README.md", "w", encoding="utf-8", errors="replace"
    ) as readme:
        data = {
            "title": question["title"],
            "package_name": python_submodule.package_name,
            "version": python_submodule.version,
            "url": python_submodule.url,
            "author": python_submodule.author,
            "author_email": python_submodule.author_email,
            "description": python_submodule.description,
            "dependencies": python_submodule.dependencies,
        }
        source = render_readme_md(data)
        readme.write(source)


def render_readme_md(
    data: Dict[str, Any],
) -> str:
    """
    Rehash other stuff and act as table of contents
    """

    template = load_template(template_filename="README.md.jinja", autoescape=False)
    # Turn off autoescape because this is python not html.
    output_text = template.render(item=data, autoescape=False)  # nosec
    # calling this to see if it is somewhat valid markdown
    _ = markdown.markdown(output_text)
    return output_text
