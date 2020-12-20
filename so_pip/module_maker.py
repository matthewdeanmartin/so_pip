import stackexchange
from bs4 import BeautifulSoup

from so_pip.code_transformations import html_to_python_comments, fix_interactive, \
    fix_shell
from so_pip.model import PythonSubmodule
from so_pip.python_validator import validate_python
from so_pip.settings import ASSUME_ONE_LINER_IS_NOT_CODE, IGNORE_SYNTAX_ERRORS
from so_pip.upgrade_to_py3 import upgrade_string


def handle_python_answer(html:str) -> PythonSubmodule:
    """Build up lines to write as list."""
    submodule = PythonSubmodule()

    regex_expression = (
        '(<pre class="lang-py prettyprint-override"><code>'
        '|<pre class="lang-python prettyprint-override"><code>'
        "|<pre><code>|</code></pre>)"
    )
    parts = stackexchange.re.split(regex_expression, html)

    in_comment = True
    for part in parts:
        if part in (
            "<pre><code>",
            '<pre class="lang-python prettyprint-override"><code>',
            '<pre class="lang-py prettyprint-override"><code>',
        ):
            in_comment = False
            continue
        if part == "</code></pre>":
            in_comment = True
            continue
        if in_comment:
            comment = html_to_python_comments(part)
            if comment:
                submodule.to_write.append(comment)
            # not in comment anymore, remove blank lines.
            submodule.strip_trailing_blank()
            continue

        # handle html escapes in what is mostly not html
        soup = BeautifulSoup(
            "<pre><code>" + part + "</pre></code>", features="html.parser"
        )
        code = soup.findAll("code")[0].text

        if ASSUME_ONE_LINER_IS_NOT_CODE and "\n" not in code:
            continue

        code = fix_interactive(code)
        code = fix_shell(code)
        code = upgrade_string(code)

        python_is_valid, errors = validate_python(code)
        if python_is_valid:
            submodule.to_write.append(code)
            submodule.all_code.append(code)
        else:
            submodule.failed_parse = True
            if IGNORE_SYNTAX_ERRORS:
                for error in errors:
                    error_message = f"# Syntax error: {error}"
                    submodule.to_write.append(error_message)
                submodule.to_write.append(code)
                submodule.all_code.append(code)

    submodule.strip_trailing_blank()
    return submodule
