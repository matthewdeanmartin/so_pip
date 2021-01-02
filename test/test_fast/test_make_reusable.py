from so_pip.parse_python.make_reusable import wrap_in_run

def test_wrap_in_run():
    result = wrap_in_run(
            """import foo
    import bar

    from baz import blerg

    print("hello world")

    """
        )
    assert result
    assert "run()" in result
