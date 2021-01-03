"""
Create a setup.py file

DEPRECATED. I MAY DELETE THIS ALTOGETHER.
"""
from typing import Dict, Sequence, Union

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import PythonPackage


def create_setup_py(package_folder: str, python_submodule: PythonPackage) -> None:
    """Just the setup.py part"""
    with open(
        package_folder + "/setup.py", "w", encoding="utf-8", errors="replace"
    ) as setup:
        data = {
            "package_name": python_submodule.package_name,
            "version": python_submodule.version,
            "url": python_submodule.url,
            "author": python_submodule.author,
            "author_email": python_submodule.author_email,
            "description": python_submodule.description,
            "dependencies": python_submodule.dependencies,
        }
        source = render_setup_py(data)
        setup.write(source)


def render_setup_py(
    data: Dict[str, Union[str, Sequence[str]]],
) -> str:
    """
    Render minimal setup.py suitable for `pip install -e .`
    """
    template = load_template(template_filename="setup.py.jinja", autoescape=False)
    # Turn off autoescape because this is python not html.
    output_text = template.render(item=data, autoescape=False)  # nosec
    return output_text
