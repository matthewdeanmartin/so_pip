"""
Load a template and apply JSON document.

There should be no domain specific logic here, just a facade over the jinja2 library
"""

import logging

from jinja2 import Environment, FileSystemLoader, Template

from so_pip.file_writing import find_file

LOGGER = logging.getLogger(__name__)

TEMPLATE_PATH = find_file("templates", __file__)


# Path(__file__) / "/templates/"


def load_template(template_filename: str = "", autoescape: bool = True) -> Template:
    """Get template from file system"""

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_PATH),
        # I'm using jina for html, MD, rst, etc
        # autoescape only escapes HTML!
        autoescape=autoescape,  # nosec
    )
    return env.get_template(f"{template_filename}")
