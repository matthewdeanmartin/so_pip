from typing import Dict, Any, Optional

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import PythonPackage
from so_pip.support_files.authors import get_authors_for_answer, \
    get_authors_for_question


def create_readme_md(package_folder: str, python_submodule: PythonPackage,
                    question: Dict[str,Any],
                    answer: Optional[Dict[str,Any]] = None,
) -> None:
    """write file"""
    authors = get_authors_for_question(question)
    if answer:
        authors.union(get_authors_for_answer(answer))

    with open(
        package_folder + "/README.md", "w", encoding="utf-8", errors="replace"
    ) as setup:
        data = {
            "title":question["title"],
            "package_name": python_submodule.package_name,
            "version": python_submodule.version,
            "url": python_submodule.url,
            "author": python_submodule.author,
            "author_email": python_submodule.author_email,
            "description": python_submodule.description,
            "dependencies": python_submodule.dependencies,
            "authors": authors
        }
        source = render_readme_md(data)
        setup.write(source)

def render_readme_md(
    data: Dict[str, Any],
) -> str:
    """
    Render minimal setup.py suitable for `pip install -e .`
    """

    template = load_template(template_filename="setup.py.jinja", autoescape=False)
    # Turn off autoescape because this is python not html.
    output_text = template.render(item=data, autoescape=False) # nosec
    return output_text
