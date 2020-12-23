"""
Load a template and apply JSON document.

There should be no domain specific logic here, just a facade over the jinja2 library
"""

import logging
from typing import Dict, Sequence, Tuple, Union

from jinja2 import Environment, FileSystemLoader, Template

from so_pip.file_writing import find_file

LOGGER = logging.getLogger(__name__)

TEMPLATE_PATH = find_file("templates", __file__)
# Path(__file__) / "/templates/"


def load_template(template_filename: str = "") -> Template:
    """Get template from file system"""

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_PATH),
        autoescape=True,  # keeps bandit happy, more secure
    )
    return env.get_template(f"{template_filename}")


def render_setup_py(
    data: Dict[str, Union[str, Sequence[str]]],
) -> str:
    """
    Render minimal setup.py suitable for `pip install -e .`
    """
    template = load_template(template_filename="setup.py.jinja")
    output_text = template.render(item=data)
    return output_text


if __name__ == "__main__":
    model = {
        "package_name": "pn",
        "version": "v",
        "url": "url",
        "author": "au",
        "author_email": "twitter",
        "description": "desc",
        "dependencies": ["a", "b"],
    }

    print(render_setup_py(model))
