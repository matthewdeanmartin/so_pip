from so_pip.parse_code.language_guessing import assign_extension


def test_assign_extension():
    extension, language = assign_extension(
        "print('hello')", False, tags=["python", "stuff"]
    )
    assert extension == ".py"
    extension, language = assign_extension("", True, tags=["python", "stuff"])
    assert extension == ".py"

    extension, language = assign_extension(
        "pip install foo", True, tags=["python", "stuff"]
    )
    assert extension == ".sh"

    # extension,language= assign_extension("public static void class Foo {System.out.println('yo')}",True)
    # assert extension==".java"
