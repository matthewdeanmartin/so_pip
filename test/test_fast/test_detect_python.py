from so_pip.language_guessing.election import guess_language_all_methods


def test_score():
    assert guess_language_all_methods(open(__file__).read())
