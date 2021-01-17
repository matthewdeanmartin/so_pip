"""
Create a code of conduct file
"""
import markdown

from so_pip.make_from_template import load_template


def render_code_of_conduct(package_folder: str) -> str:
    """
    Links to SO's code of conduct
    """
    template = load_template(
        template_filename="CODE_OF_CONDUCT.md.jinja", autoescape=False
    )
    output_text = template.render()
    # check if markdown is okay
    _ = markdown.markdown(output_text)
    with open(
        package_folder + "/CODE_OF_CONDUCT.md", "w", encoding="utf-8", errors="replace"
    ) as author_file:
        author_file.write(output_text)

    return output_text
