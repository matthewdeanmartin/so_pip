"""
Create ini file for setup.py.

The setup.cfg file is weird. It can only override values in setup.py
and is used by some tools as a centralized config.ini file.
"""
import configparser
from typing import Any, Dict

from so_pip.make_from_template import load_template
from so_pip.models.python_package_model import PythonPackage


def create_setup_cfg(package_folder: str, python_submodule: PythonPackage) -> None:
    """Put everything into setup.cfg"""
    full_path = package_folder + "/setup.cfg"
    with open(full_path, "w", encoding="utf-8", errors="replace") as setup_cfg:
        post_id = 0
        data = {
            "package_name": python_submodule.package_name,
            "version": python_submodule.version,
            "url": python_submodule.url,
            "author": python_submodule.author,
            "author_email": python_submodule.author_email,
            "description": python_submodule.description,
            "dependencies": python_submodule.dependencies,
            "classifiers": """    Programming Language :: Python :: 3 :: Only
            Programming Language :: Python :: 3.6
            Programming Language :: Python :: 3.7
            Programming Language :: Python :: 3.8
            Programming Language :: Python :: 3.9""",
            "revisions_url": f"https://stackoverflow.com/posts/{post_id}/revisions",
        }
        source = render_setup_cfg(data)

        setup_cfg.write(source)
        config = configparser.ConfigParser()
        _ = config.read(full_path)

    with open(
        package_folder + "/setup.py", "w", encoding="utf-8", errors="replace"
    ) as setup_py:
        template = load_template(
            template_filename="setup_bare.py.jinja", autoescape=False
        )
        # Turn off autoescape because this is python not html.
        output_text = template.render(item=data, autoescape=False)  # nosec
        setup_py.write(output_text)


def render_setup_cfg(
    data: Dict[str, Any],
) -> str:
    """
    Render minimal setup.py suitable for `pip install -e .`
    """
    template = load_template(template_filename="setup.cfg.jinja", autoescape=False)
    # Turn off autoescape because this is python not html.
    output_text = template.render(item=data, autoescape=False)  # nosec
    return output_text
