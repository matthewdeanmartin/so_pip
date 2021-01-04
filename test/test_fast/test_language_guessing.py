from so_pip.language_guessing.election import guess_language_all_methods
from so_pip.language_guessing.keyword_based import guess_by_keywords
from so_pip.language_guessing.language_guessing import assign_extension
from so_pip.language_guessing.regex_based import language_by_regex_features


def test_assign_extension():
    extension, language = assign_extension("print('hello')", tags=["python", "stuff"])
    assert extension == ".py"
    extension, language = assign_extension("", tags=["python", "stuff"])
    assert extension == ".py"

    # bash is hard to guess.
    extension, language = assign_extension("pip install foo", tags=["python", "stuff"])
    assert extension == ".py"

    # extension,language= assign_extension("public static void class Foo {System.out.println('yo')}",True)
    # assert extension==".java"


def test_election():
    assert guess_language_all_methods(
        "public static void main(args[]){\n   system.out.writeln('');}"
    )
    assert guess_language_all_methods("def yo():\n   print('hello')", file_name="yo.py")

    assert guess_language_all_methods("sudo yum install pip", file_name="foo.sh")
    assert guess_language_all_methods(
        "sudo yum install pip", surrounding_text="The file is named foo.py"
    )


def test_guess_by_keywords():
    assert "python" in guess_by_keywords("def class pip")


def test_language_by_regex_features():
    assert "python" in language_by_regex_features("def foo():\n   print('yo')")
