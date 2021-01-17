"""
Authors file

This is roughly following Gnu Gnit's conventions.

Also draws inspiration from google's format.
https://opensource.google/docs/releasing/authors/

Also draws inspiration from libraries that attempt to parse AUTHORS files.
https://www.npmjs.com/package/stringify-author
https://www.npmjs.com/package/author-regex
"""
import logging
from collections import defaultdict
from typing import Any, Collection, DefaultDict, Dict, List, Optional, Sequence, Union

import markdown

from so_pip.make_from_template import load_template
from so_pip.models.authors_model import (
    Author,
    bind_answer_to_authors,
    bind_question_to_authors,
)

LOGGER = logging.getLogger(__name__)


def write_authors(
    package_folder: str,
    package_name: str,
    question: Dict[str, Any],
    answer: Optional[Dict[str, Any]] = None,
) -> None:
    """write file"""
    if answer:
        authors = bind_answer_to_authors(answer, question)
    else:
        authors = bind_question_to_authors(question)

    sections: DefaultDict[str, List[Author]] = defaultdict(list)
    for author in authors.everyone:
        for role in author.roles:
            if author not in sections[role]:
                sections[role].append(author)
    for _, value in sections.items():
        value.sort(key=lambda _: _.display_name.lower())
    for author in authors.everyone:
        author.urls.sort(key=lambda _: "" if "stackoverflow.com" in _ else _.lower())

    with open(
        package_folder + "/AUTHORS.md", "w", encoding="utf-8", errors="replace"
    ) as author_file:
        item = {"name": package_name, "authors": sections}
        text = render_authors(data=item)
        # calling this to see if it is somewhat valid markdown
        _ = markdown.markdown(text)
        author_file.write(text)


def render_authors(
    data: Dict[str, Union[str, Sequence[str], Collection[str]]],
) -> str:
    """
    Render minimal setup.py suitable for `pip install -e .`
    """
    template = load_template(template_filename="AUTHORS.jinja", autoescape=False)
    output_text = template.render(item=data)
    return output_text
