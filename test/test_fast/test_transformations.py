from so_pip.parse_python.code_transformations import (
    fix_interactive,
    fix_shell,
    wrap_with_run,
)


def test_fix_shell():
    assert fix_shell("$ dir") == "# $ dir"
    assert fix_shell("pip install requests") == "# pip install requests"


def test_fix_interactive():
    assert fix_interactive(">>> abc") == "abc"
    assert fix_interactive("... abc") == "abc"
    assert fix_interactive("> abc") == "# > abc"
    assert fix_interactive(">> abc") == "# >> abc"

    assert fix_interactive(">>>") == ""
    assert fix_interactive("...") == ""


def test_wrap_with_run():
    wrapped = "def run() -> None:\n    print('hello')"
    assert wrap_with_run("""print('hello')""") == wrapped
