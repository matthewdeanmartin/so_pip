"""
Create a setup.py file
"""
from typing import Dict, Sequence, Union

from so_pip.make_from_template import load_template


def render_setup_py(
    data: Dict[str, Union[str, Sequence[str]]],
) -> str:
    """
    Render minimal setup.py suitable for `pip install -e .`
    """
    template = load_template(template_filename="setup.py.jinja", autoescape=False)
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
